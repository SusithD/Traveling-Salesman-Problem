import random
import time
import matplotlib.pyplot as plt
import numpy as np
from city import City
from algorithms import brute_force, dynamic_programming, nearest_neighbor
from database import save_game_results, get_all_results
from ui import display_menu, get_player_name, display_cities, get_selected_cities, display_route
from exceptions import InvalidSelectionError, DatabaseError

def initialize_cities():
    """Initialize 10 cities (A to J) with random coordinates."""
    cities = {}
    for city_id in range(65, 75):  # ASCII values for A to J
        city_name = chr(city_id)
        # Random coordinates between 0 and 100
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        cities[city_name] = City(city_name, x, y)
    return cities

def calculate_distances(cities):
    """Calculate distances between all cities and return distance matrix."""
    city_names = list(cities.keys())
    num_cities = len(city_names)
    distances = {}
    
    for i in range(num_cities):
        city1 = city_names[i]
        distances[city1] = {}
        for j in range(num_cities):
            city2 = city_names[j]
            if i == j:
                distances[city1][city2] = 0
            else:
                # Random distance between 50 and 100 km
                distances[city1][city2] = random.randint(50, 100)
    
    return distances

def play_game():
    """Main game function."""
    try:
        player_name = get_player_name()
        cities = initialize_cities()
        distances = calculate_distances(cities)
        
        # Select random home city
        home_city = random.choice(list(cities.keys()))
        print(f"Home city for this round is: {home_city}")
        
        display_cities(cities, distances)
        
        # Get player's city selections
        selected_cities = get_selected_cities(cities, home_city)
        
        if not selected_cities:
            print("No cities selected. Returning to menu.")
            return
        
        # Run algorithms and measure time
        algorithms = {
            "Brute Force": brute_force,
            "Dynamic Programming": dynamic_programming,
            "Nearest Neighbor": nearest_neighbor
        }
        
        results = {}
        for name, algorithm in algorithms.items():
            start_time = time.time()
            route, distance = algorithm(distances, home_city, selected_cities)
            end_time = time.time()
            execution_time = end_time - start_time
            
            results[name] = {
                "route": route,
                "distance": distance,
                "time": execution_time
            }
            
            print(f"\n{name} Algorithm:")
            print(f"Route: {' -> '.join(route)}")
            print(f"Total distance: {distance} km")
            print(f"Execution time: {execution_time:.6f} seconds")
        
        # Get shortest route
        shortest = min(results.values(), key=lambda x: x['distance'])
        shortest_algo = [k for k, v in results.items() if v['distance'] == shortest['distance']][0]
        
        print(f"\nShortest route found by {shortest_algo}: {' -> '.join(shortest['route'])}")
        print(f"Distance: {shortest['distance']} km")
        
        # Display the route
        display_route(cities, shortest['route'])
        
        # Player guess and database saving
        save_game_results(
            player_name, 
            home_city, 
            selected_cities,
            shortest['route'], 
            shortest['distance'],
            {algo: data['time'] for algo, data in results.items()}
        )
        
        print("\nResults saved to database!")
        
    except InvalidSelectionError as e:
        print(f"Error: {e}")
    except DatabaseError as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def main():
    while True:
        choice = display_menu()
        
        if choice == '1':
            play_game()
        elif choice == '2':
            results = get_all_results()
            # Display results
            for result in results:
                print(result)
        elif choice == '3':
            # Show algorithm analysis
            print("\nAlgorithm Complexity Analysis:")
            print("1. Brute Force: O(n!)")
            print("2. Dynamic Programming: O(n²·2ⁿ)")
            print("3. Nearest Neighbor: O(n²)")
            print("\nPress Enter to continue...")
            input()
        elif choice == '4':
            print("Thank you for playing!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
