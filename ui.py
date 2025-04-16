import matplotlib.pyplot as plt
import networkx as nx
from exceptions import InvalidSelectionError

def display_menu():
    """Display the main menu and return the user's choice."""
    print("\n===== Traveling Salesman Problem Game =====")
    print("1. Play New Game")
    print("2. View Past Results")
    print("3. Algorithm Analysis")
    print("4. Exit")
    return input("Enter your choice (1-4): ")

def get_player_name():
    """Get the player's name."""
    while True:
        name = input("\nEnter your name: ").strip()
        if name:
            return name
        print("Name cannot be empty. Please try again.")

def display_cities(cities, distances):
    """Display the cities and distances between them."""
    print("\nCity Locations:")
    for city_name, city in cities.items():
        print(f"{city_name}: ({city.x}, {city.y})")
    
    print("\nDistance Matrix (in km):")
    city_names = sorted(cities.keys())
    
    # Print header
    header = "    " + "  ".join(f"{city:^4}" for city in city_names)
    print(header)
    
    # Print distances
    for city1 in city_names:
        row = f"{city1}  "
        for city2 in city_names:
            row += f"{distances[city1][city2]:^4} "
        print(row)
    
    # Create a visualization of the cities and connections
    plt.figure(figsize=(8, 8))
    
    # Plot city positions
    for city_name, city in cities.items():
        plt.plot(city.x, city.y, 'o', markersize=10)
        plt.text(city.x, city.y + 2, city_name, fontsize=12, ha='center')
    
    plt.xlim(-10, 110)
    plt.ylim(-10, 110)
    plt.title("City Positions")
    plt.grid(True)
    plt.show()

def get_selected_cities(cities, home_city):
    """Get the cities selected by the player."""
    print(f"\nHome city is {home_city}. You must visit at least one other city.")
    print("Available cities: " + ", ".join([c for c in cities.keys() if c != home_city]))
    
    while True:
        selection = input("Enter the cities you want to visit (e.g., A,C,E) or 'all' for all cities: ").strip().upper()
        
        if selection.lower() == 'all':
            return [c for c in cities.keys() if c != home_city]
        
        selected = [c.strip() for c in selection.split(',') if c.strip()]
        
        # Validate selections
        invalid = [c for c in selected if c not in cities.keys()]
        if invalid:
            print(f"Invalid cities: {', '.join(invalid)}. Please try again.")
            continue
            
        if home_city in selected:
            print(f"Home city {home_city} is already the start/end point. No need to include it.")
            selected.remove(home_city)
            
        if not selected:
            print("You must select at least one city to visit.")
            continue
            
        return selected

def display_route(cities, route):
    """Display the route graphically."""
    plt.figure(figsize=(8, 8))
    
    # Plot city positions
    for city_name, city in cities.items():
        if city_name == route[0]:  # Home city
            plt.plot(city.x, city.y, 'o', markersize=12, color='red')
        else:
            plt.plot(city.x, city.y, 'o', markersize=10, color='blue')
        plt.text(city.x, city.y + 2, city_name, fontsize=12, ha='center')
    
    # Plot the route
    for i in range(len(route) - 1):
        city1 = cities[route[i]]
        city2 = cities[route[i+1]]
        plt.plot([city1.x, city2.x], [city1.y, city2.y], 'k-', linewidth=1.5)
        # Add arrow to show direction
        mid_x = (city1.x + city2.x) / 2
        mid_y = (city1.y + city2.y) / 2
        plt.annotate('', xy=(city2.x, city2.y), xytext=(mid_x, mid_y), 
                    arrowprops=dict(arrowstyle='->', lw=1.5, color='red'))
    
    plt.xlim(-10, 110)
    plt.ylim(-10, 110)
    plt.title("TSP Route: " + " -> ".join(route))
    plt.grid(True)
    plt.show()
