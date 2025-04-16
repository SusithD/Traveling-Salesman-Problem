# Traveling Salesman Problem Game

A Python implementation of the Traveling Salesman Problem (TSP) as an interactive game. Players can select cities to visit, and the game will find the shortest route using three different algorithms:

- Brute Force (exact solution, O(n!))
- Dynamic Programming (exact solution, O(n²·2ⁿ))
- Nearest Neighbor (approximation, O(n²))

## Features

- Random city generation with distances ranging from 50-100 km
- Visual representation of cities and routes using matplotlib
- Performance measurement of different TSP algorithms
- Game results saved to a local database
- Detailed algorithm analysis

## Requirements

- Python 3.6+
- matplotlib
- numpy
- networkx

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/tsp-game.git
   cd tsp-game
   ```

2. Create a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the game with:
```
python tsp_game.py
```

## Project Structure

- `tsp_game.py`: Main application file
- `city.py`: City class definition
- `algorithms.py`: TSP algorithm implementations
- `ui.py`: User interface functions
- `database.py`: Database management
- `exceptions.py`: Custom exceptions
- `test_tsp_game.py`: Unit tests

## License

MIT
