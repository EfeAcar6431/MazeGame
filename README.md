# Graph Maze Game

## Overview
Graph Maze Game is a Python-based game built with Pygame where the player navigates a graph structure to find hidden treasure before a snake bot does. The game ends when either the player or the snake reaches the treasure.

![Graph Maze Game](https://github.com/EfeAcar6431/MazeGame/blob/main/MazeGameScreen.png)

## Objective
- Find the treasure before the snake bot does.
- If the player reaches the treasure first, they win.
- If the snake bot reaches the treasure first, the player loses.

## Features
- **Graph-based Maze:** The game is structured as a graph where nodes represent positions and edges represent possible movements.
- **Different Difficulty Levels:** Players can choose from Easy, Normal, and Hard difficulty, each affecting the size and complexity of the graph.
- **AI Opponent:** The snake bot navigates the graph using either Depth-First Search (DFS) or Breadth-First Search (BFS), chosen randomly.
- **User-friendly Interface:** Main menu, difficulty selection, rules menu, and game over screen are implemented.

## Controls
- `W` - Move up
- `A` - Move left
- `S` - Move down
- `D` - Move right

## Game States
1. **Main Menu**: Choose to start the game, view rules, or exit.
2. **Difficulty Selection**: Select difficulty level (Easy, Normal, or Hard).
3. **Gameplay**: Navigate through the graph and race the bot to the treasure.
4. **Rules Menu**: View instructions on how to play.
5. **End Screen**: Displays the win/loss message.

## How to Play
1. Launch the game and navigate through the menus.
2. Choose your desired difficulty level.
3. Move through the graph using `W`, `A`, `S`, `D` keys.
4. Reach the treasure before the snake bot does.
5. The game ends once the treasure is found.

## Dependencies
- Python 3
- Pygame

## Installation
1. Install Python 3 if not already installed.
2. Install Pygame using:
   ```sh
   pip install pygame
   ```
3. Run the game script:
   ```sh
   python graph_maze_game.py
   ```

## Future Improvements
- Implement different AI strategies for the bot.
- Add more complex graph structures.
- Introduce power-ups or obstacles to increase gameplay variety.

Enjoy the game!
