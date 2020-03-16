import pygame
import sys

# Field size
size = 400, 600

# Convenience constants for size
WIDTH = 0
HEIGHT = 1

# Some colors for the visualization
black = 0,0,0
red = 255,0,0
fertile_plot_colors = [(0,175,0), (100,200,100)]

test_input_0 = {}

test_input_1 = {"0 292 399 307"}
# Expected output: 116800 116800

test_input_2 = {"48 192 351 207",
                "48 392 351 407",
                "120 52 135 547",
                "260 52 275 547"}
# Expected output: 22816 192608

test_input_3 = {"0 5 9 6"}


# Parse the input to get the rects into a format Pygame prefers
# Returns an array of Pygame.rect objects
def parse_rects(rect_set):
    parsed_rects = []

    for rect_string in rect_set:
        string_tokens = rect_string.split()
        rect = pygame.Rect(
                int(string_tokens[0]),
                size[HEIGHT] - int(string_tokens[3]) - 1, # Flip the Y-origin
                int(string_tokens[2]) - int(string_tokens[0]) + 1,
                int(string_tokens[3]) - int(string_tokens[1]) + 1)
        parsed_rects.append(rect)

    return parsed_rects


# Returns True if point is contained within rect
def rect_contains_point(rect, point):
    x = point[0]
    y = point[1]

    if x >= rect.x and x < rect.x + rect.width:
        if y >= rect.y and y < rect.y + rect.height:
            return True

    return False


# Returns True if point is contained within any of the rects provided
def rects_contain_point(rects, point):
    for rect in rects:
        if rect_contains_point(rect, point):
            return True

    return False

# Convenience method to add context to method call
def is_barren(barren_rects, point):
    return rects_contain_point(barren_rects, point)


# Given a point, return a set of orthogonally-adjacent neighbors within the
#   bounds of the grid
def add_neighbors(point, set_to_be_modified):
    x = point[0]
    y = point[1]

    if x > 0:
        set_to_be_modified.add((x - 1, y))
    if x < size[WIDTH] - 1:
        set_to_be_modified.add((x + 1, y))
    if y > 0:
        set_to_be_modified.add((x, y - 1))
    if y < size[HEIGHT] - 1:
        set_to_be_modified.add((x, y + 1))


# Use Pygame to visually display barren and fertile land
def display_results(barren_rects, fertile_plots):
    pygame.init()
    pygame.display.set_caption("Barren Land Analysis")
    screen = pygame.display.set_mode(size)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        screen.fill(black)

        for rect in barren_rects:
            pygame.draw.rect(screen, red, rect)

        color_index = 0
        for plot in completed_fertile_plots:
            for point in plot:
                point_rect = pygame.Rect(point[0], point[1], 1, 1)
                # Different green for each fertile plot looks nice
                screen.fill(fertile_plot_colors[color_index], point_rect)

            color_index += 1

        pygame.display.flip()

# Given an origin point, find the set of contiguous points that aren't barren
def find_contiguous_land(origin, barren_rects, barren_land, fertile_land):
    current_fertile_plot = set()
    current_fertile_plot.add(origin)
    fertile_land.add(origin)

    test_set = set()
    add_neighbors(origin, test_set)

    while len(test_set) > 0:
        point = test_set.pop()
        if point not in fertile_land and point not in barren_land:
            if not is_barren(barren_rects, point):
                fertile_land.add(point)
                current_fertile_plot.add(point)
                add_neighbors(point, test_set)
            else:
                barren_land.add(point)

    return current_fertile_plot

# Find the size of each fertile plot and print in ascending order
def print_fertile_plots(fertile_plots):
    fertile_plot_sizes = []
    for plot in fertile_plots:
        fertile_plot_sizes.append(len(plot))

    sorted_fertile_plot_sizes = sorted(fertile_plot_sizes)
    plot_string = ""
    for plot in sorted_fertile_plot_sizes:
        plot_string += str(plot) + " "

    print(plot_string)

# Main

test_input = eval(sys.stdin.read())
barren_rects = parse_rects(test_input)

barren_land = set()
fertile_land = set()
completed_fertile_plots = []

for x in range(0, size[WIDTH]):
    for y in range(0, size[HEIGHT]):
        point = (x,y)
        if is_barren(barren_rects, point):
            barren_land.add(point)
        elif point not in fertile_land:
            fertile_plot = find_contiguous_land(point,
                                                barren_rects,
                                                barren_land,
                                                fertile_land)
            if len(fertile_plot) > 0:
                completed_fertile_plots.append(fertile_plot)

print_fertile_plots(completed_fertile_plots)

#display_results(barren_rects, completed_fertile_plots)
