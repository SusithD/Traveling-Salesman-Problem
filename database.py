import sqlite3
import os
import json
from exceptions import DatabaseError

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tsp_game.db')

def initialize_db():
    """Initialize the database if it doesn't exist."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create game_results table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            home_city TEXT NOT NULL,
            selected_cities TEXT NOT NULL,
            shortest_route TEXT NOT NULL,
            total_distance REAL NOT NULL,
            execution_times TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        raise DatabaseError(f"Database initialization failed: {e}")

def save_game_results(player_name, home_city, selected_cities, shortest_route, distance, execution_times):
    """Save game results to the database."""
    try:
        initialize_db()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO game_results 
        (player_name, home_city, selected_cities, shortest_route, total_distance, execution_times)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            player_name,
            home_city,
            json.dumps(selected_cities),
            json.dumps(shortest_route),
            distance,
            json.dumps(execution_times)
        ))
        
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        raise DatabaseError(f"Failed to save game results: {e}")

def get_all_results():
    """Get all game results from the database."""
    try:
        initialize_db()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT id, player_name, home_city, selected_cities, shortest_route, total_distance, 
               execution_times, timestamp
        FROM game_results
        ORDER BY timestamp DESC
        ''')
        
        results = []
        for row in cursor.fetchall():
            id, player, home, selected, route, distance, times, timestamp = row
            
            result = {
                'id': id,
                'player_name': player,
                'home_city': home,
                'selected_cities': json.loads(selected),
                'shortest_route': json.loads(route),
                'total_distance': distance,
                'execution_times': json.loads(times),
                'timestamp': timestamp
            }
            results.append(result)
            
        conn.close()
        return results
    except sqlite3.Error as e:
        raise DatabaseError(f"Failed to retrieve game results: {e}")

def get_algorithm_performance():
    """Get performance data for all algorithms."""
    try:
        initialize_db()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT execution_times FROM game_results')
        
        performance_data = {
            'Brute Force': [],
            'Dynamic Programming': [],
            'Nearest Neighbor': []
        }
        
        for row in cursor.fetchall():
            times = json.loads(row[0])
            for algo, time in times.items():
                if algo in performance_data:
                    performance_data[algo].append(time)
        
        conn.close()
        return performance_data
    except sqlite3.Error as e:
        raise DatabaseError(f"Failed to retrieve algorithm performance data: {e}")
