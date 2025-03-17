"""
This program creates a graph maze game with the objective of finding the treasure in the end. If you the player find it
first then you win, but if the snake finds it first you lose. The program ends when the treasure is found.
"""
import pygame
import sys
import math
import random
from collections import defaultdict


# This initializes Pygame
pygame.init()

# This is to set up the screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Graph Game')

# Colors and Fonts
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (240, 0, 255)
MAROON = (115, 0, 0)
MAGENTA = (255, 0, 230)

# These variables are for the fonts of the text on the buttons
font = pygame.font.Font(None, 36)
rules_font = pygame.font.Font(None, 20)
large_font = pygame.font.Font(None, 72)
back_font = pygame.font.Font(None, 80)

# This is how the states are handled with the first state being set as the main menu
MAIN_MENU = 1
DIFFICULTY_MENU = 2
GAMEPLAY = 3
RULES_MENU = 4
# Starting State
state = MAIN_MENU

# The difficulty is initialized as Easy
difficulty = 'Easy'

# The graph is made up of nodes and edges with these lengths and the user position is initialized as the start.
node_radius = 10
user_radius = 5
nodes = []
edges = []
user_position = 0

# These are the values for the snake bot
bot_position = 0
bot_algorithm = random.choice(['DFS', 'BFS'])
bot_move_timer = 0
bot_generator = None
graph = None


# Function to draw button
def draw_button(text, button_rect, color, is_back_button=False):
    if not is_back_button:
        pygame.draw.rect(screen, color, button_rect)
    text_surf = (back_font if is_back_button else font).render(text, True, BLUE if is_back_button else BLACK)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)

def write_text(txt, pos, type):
    if type == "title":
        text_surf = large_font.render(txt, True, BLUE)
    else:
        text_surf = rules_font.render(txt, True, RED)
    text_rect = text_surf.get_rect(center=pos)
    screen.blit(text_surf, text_rect)



# Create a tree structure based on difficulty
# The node and edge arrays for the difficulties were generated to follow the models of a tree graph
def create_tree():
    global nodes, edges
    positions = []
    edges = []

    # These coordinates were generated by an LLM for the graphs so that the edges between any two nodes is equidistant.
    if difficulty == 'Easy':
        # This will create a graph tree with 8 nodes for Easy difficulty
        positions = [(100, 500), (200, 400), (300, 300), (400, 200), (500, 300), (400, 400), (300, 500), (200, 500)]
        edges = [(0, 1), (1, 2), (2, 3), (3, 4), (2, 5), (5, 6), (6, 7)]
    elif difficulty == 'Normal':
        # This will create a graph tree with 10 nodes for Normal difficulty
        positions = [(100, 500), (200, 400), (300, 300), (400, 200), (500, 100), (600, 200), (700, 300), (600, 400),
                     (500, 500), (400, 400)]
        edges = [(0, 1), (1, 2), (2, 3), (3, 4), (3, 5), (5, 6), (6, 7), (7, 8), (7, 9)]
    elif difficulty == 'Hard':
        # This will create a graph tree with 12 nodes for Hard difficulty
        positions = [
            (50, 500), (150, 400), (250, 300),
            (350, 200), (450, 100), (550, 200),
            (650, 300), (750, 400), (650, 500),
            (550, 400), (450, 300), (350, 400)]
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 4), (3, 5), (5, 6), (6, 7),
            (7, 8), (6, 9), (5, 10), (10, 11)]

    nodes = positions

# This draws the graph with special handling for the treasure node
def draw_graph():
    for edge in edges:
        start_pos = nodes[edge[0]]
        end_pos = nodes[edge[1]]
        pygame.draw.line(screen, BLACK, start_pos, end_pos, 2)

    for i, node in enumerate(nodes):
        if i == treasure_node and (user_position == treasure_node or bot_position == treasure_node):
            # If the node is the treasure and it's found, draw it larger and in yellow
            pygame.draw.circle(screen, YELLOW, node, node_radius + 20)
        else:
            pygame.draw.circle(screen, RED, node, node_radius)

# Draw the user
def draw_user():
    global user_position
    pygame.draw.circle(screen, BLUE, nodes[user_position], user_radius)

# Update user position
def move_user(direction):
    global user_position
    current_node_pos = nodes[user_position]

    # Get directly connected nodes
    directly_connected_nodes = [edge[1] if edge[0] == user_position else edge[0] for edge in edges if user_position in edge]
    if direction in ['A', 'D']:
        # Handling left and right movements
        best_node_index = None
        min_vertical_distance = float('inf')

        for other_node_index in directly_connected_nodes:
            other_node_pos = nodes[other_node_index]

            dx = other_node_pos[0] - current_node_pos[0]
            dy = other_node_pos[1] - current_node_pos[1]

            if (direction == 'A' and dx < 0) or (direction == 'D' and dx > 0):
                vertical_distance = abs(dy)
                if vertical_distance < min_vertical_distance:
                    min_vertical_distance = vertical_distance
                    best_node_index = other_node_index

        if best_node_index is not None:
            user_position = best_node_index

    elif direction == 'S' and difficulty == 'Hard':
        # Special case for 'S' in Hard difficulty
        downward_nodes = []
        min_vertical_distance = float('inf')

        for other_node_index in directly_connected_nodes:
            other_node_pos = nodes[other_node_index]

            dy = other_node_pos[1] - current_node_pos[1]
            if dy > 0:  # Node is below
                vertical_distance = abs(dy)
                if vertical_distance <= min_vertical_distance:
                    if vertical_distance < min_vertical_distance:
                        downward_nodes.clear()
                        min_vertical_distance = vertical_distance
                    downward_nodes.append((other_node_index, other_node_pos[0]))

        if downward_nodes:
            # Choose the leftmost node among equidistant nodes
            user_position = min(downward_nodes, key=lambda x: x[1])[0]

    else:
        # Handling up and down movements for all difficulties except 'S' in Hard
        for other_node_index in directly_connected_nodes:
            other_node_pos = nodes[other_node_index]

            dy = other_node_pos[1] - current_node_pos[1]

            if (direction == 'W' and dy < 0) or (direction == 'S' and dy > 0):
                user_position = other_node_index

# Convert Edges to Graph (for DFS and BFS)
def edges_to_graph(edges):
    graph = defaultdict(list)
    for start, end in edges:
        graph[start].append(end)
        graph[end].append(start)
    return graph

# Depth First Search (DFS) Generator
def dfs_generator(graph, start):
    visited = set()
    stack = [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            yield vertex
            stack.extend(set(graph[vertex]) - visited)

# Breadth First Search (BFS) Generator
def bfs_generator(graph, start):
    visited = set()
    queue = [start]
    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            yield vertex
            queue.extend(set(graph[vertex]) - visited)




# Add a global variable for the treasure node
treasure_node = None


# This sets the difficulty and creates a tree, it also chooses a random node to be the treasure goal
def set_difficulty_and_create_tree(selected_difficulty):
    global difficulty, treasure_node, user_position, graph, bot_generator
    difficulty = selected_difficulty
    create_tree()
    possible_treasure_nodes = [i for i in range(len(nodes)) if i > 2]
    treasure_node = random.choice(possible_treasure_nodes)
    user_position = 0
    bot_position = 0
    graph = edges_to_graph(edges)
    bot_generator = dfs_generator(graph, bot_position) if bot_algorithm == 'DFS' else bfs_generator(graph, bot_position)

# Display Win or Loss Screen
def display_end_screen(message, color):
    screen.fill(GREEN)
    end_text = large_font.render(message, True, color)
    text_rect = end_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(end_text, text_rect)
    pygame.display.flip()
    pygame.time.wait(5000)  # Wait for 5 seconds and then end the game

# This function is used to draw the buttons for the main screen
def make_main_mn():
    write_text("Graph Game", (screen_width // 2, 150), "title")
    draw_button("Start", start_button, GREEN)
    draw_button("Rules", rules_button, MAGENTA)
    draw_button("End", end_button, RED)

# This function is used to draw the buttons for the difficulty screen
def make_diff_mn():
    write_text("Game Difficulty", (screen_width // 2, 100), "title")
    draw_button("<", back_button, CYAN, is_back_button=True)
    draw_button("Easy", easy_button, GREEN)
    draw_button("Normal", normal_button, YELLOW)
    draw_button("Hard", hard_button, RED)

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(CYAN)
    if state == MAIN_MENU:
        start_button = pygame.Rect(300, 250, 200, 50)
        rules_button = pygame.Rect(300, 350, 200, 50)
        end_button = pygame.Rect(300, 450, 200, 50)
        make_main_mn()
    elif state == DIFFICULTY_MENU:
        back_button = pygame.Rect(20, 20, 50, 50)
        easy_button = pygame.Rect(300, 200, 200, 50)
        normal_button = pygame.Rect(300, 300, 200, 50)
        hard_button = pygame.Rect(300, 400, 200, 50)
        make_diff_mn()
    elif state == RULES_MENU:
        back_button = pygame.Rect(20, 20, 50, 50)
        draw_button("<", back_button, CYAN, is_back_button=True)
        write_text("Game Rules", (screen_width // 2, 100), "title")
        rules_box = pygame.Rect(200, 150, 400, 400)
        draw_button("", rules_box, "WHITE")
        write_text("Your task is to find the hidden treasure on one of the nodes. ", (screen_width // 2, 200), "txt")
        write_text("However there is a search snake chasing the same treasure!", (screen_width // 2, 250), "txt")
        write_text("Beat the snake to the treasure to win.", (screen_width // 2, 300), "txt")
        write_text("Use WASD to move through the graph.", (screen_width // 2, 350), "txt")


    elif state == GAMEPLAY:
        if bot_algorithm == "BFS":
            display_algorithm = font.render("You're racing against the Breadth-First Search Snake", True, PURPLE)
        else:
            display_algorithm = font.render("You're racing against the Depth-First Search Snake", True, PURPLE)

        # Here the snake type is displayed and the map is drawn
        screen.blit(display_algorithm, (10, 10))
        draw_graph()
        draw_user()
        # The size of the snake bot is slightly larger than the user
        pygame.draw.circle(screen, PURPLE, nodes[bot_position], user_radius + 2)

        bot_move_timer += clock.get_time()
        # The bot moves every 1 second
        if bot_move_timer >= 1000:
            try:
                bot_position = next(bot_generator)
                bot_move_timer = 0
            except StopIteration:
                pass

        if bot_position == treasure_node:
            draw_graph()
            pygame.time.wait(2000) # Waits 1 second to allow user to process where the treasure was.
            display_end_screen("You lost!", RED)
            break

        if user_position == treasure_node:
            draw_graph()
            pygame.time.wait(2000)  # Waits 1 second to allow user to process where the treasure was.
            display_end_screen("You found the treasure!", YELLOW)
            break

    # This for loop and the branching conditionals control which menu and options the user is choosing to initialize
    # the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if state == MAIN_MENU:
                if start_button.collidepoint(event.pos):
                    state = DIFFICULTY_MENU
                elif rules_button.collidepoint(event.pos):
                    state = RULES_MENU
                elif end_button.collidepoint(event.pos):
                    running = False
            elif state == DIFFICULTY_MENU:
                if back_button.collidepoint(event.pos):
                    state = MAIN_MENU
                elif easy_button.collidepoint(event.pos):
                    set_difficulty_and_create_tree('Easy')
                    state = GAMEPLAY
                elif normal_button.collidepoint(event.pos):
                    set_difficulty_and_create_tree('Normal')
                    state = GAMEPLAY
                elif hard_button.collidepoint(event.pos):
                    set_difficulty_and_create_tree('Hard')
                    state = GAMEPLAY
            elif state == RULES_MENU:
                if back_button.collidepoint(event.pos):
                    state = MAIN_MENU
        # The game controls are WASD
        elif event.type == pygame.KEYDOWN and state == GAMEPLAY:
            key = event.unicode.upper()
            if key in ['W', 'A', 'S', 'D']:
                move_user(key)

    pygame.display.flip()
    # This will limit the frames to 60 per second
    clock.tick(60)

# This ends the program
pygame.quit()
sys.exit()
