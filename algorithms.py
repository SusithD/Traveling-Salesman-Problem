import itertools
import sys

def brute_force(distances, home_city, cities):
    """
    Solve TSP using brute force (exact solution).
    Time complexity: O(n!)
    
    Args:
        distances: Dictionary of distances between cities
        home_city: Starting and ending city
        cities: List of cities to visit
    
    Returns:
        Tuple of (best_route, shortest_distance)
    """
    if not cities:
        return [home_city, home_city], 0
    
    cities_to_visit = cities.copy()
    if home_city in cities_to_visit:
        cities_to_visit.remove(home_city)
        
    min_distance = float('inf')
    best_route = None
    
    # Try all possible permutations
    for perm in itertools.permutations(cities_to_visit):
        current_distance = 0
        route = [home_city] + list(perm) + [home_city]
        
        # Calculate route distance
        for i in range(len(route) - 1):
            current_distance += distances[route[i]][route[i+1]]
            
        if current_distance < min_distance:
            min_distance = current_distance
            best_route = route
            
    return best_route, min_distance

def dynamic_programming(distances, home_city, cities):
    """
    Solve TSP using dynamic programming (Held-Karp algorithm).
    Time complexity: O(n²·2ⁿ)
    
    Args:
        distances: Dictionary of distances between cities
        home_city: Starting and ending city
        cities: List of cities to visit
        
    Returns:
        Tuple of (best_route, shortest_distance)
    """
    if not cities:
        return [home_city, home_city], 0
    
    cities_to_visit = cities.copy()
    if home_city in cities_to_visit:
        cities_to_visit.remove(home_city)
        
    # Convert to numeric indices for easier handling
    all_cities = [home_city] + cities_to_visit
    n = len(all_cities)
    
    # Create lookup dictionaries
    city_to_idx = {city: i for i, city in enumerate(all_cities)}
    idx_to_city = {i: city for i, city in enumerate(all_cities)}
    
    # Create distance matrix
    dist_matrix = [[distances[idx_to_city[i]][idx_to_city[j]] for j in range(n)] for i in range(n)]
    
    # Initialize memoization tables
    # dp[mask][i] = minimum distance of a path that visits all cities in mask and ends at city i
    dp = {}
    parent = {}
    
    # Initialize base case: starting from home city (index 0) to each city
    for i in range(1, n):
        dp[(1 << i) | 1, i] = dist_matrix[0][i]
        parent[(1 << i) | 1, i] = 0
        
    # Iterate through all possible subsets of cities
    for subset_size in range(2, n):
        for subset in itertools.combinations(range(1, n), subset_size):
            # Create bit mask for this subset
            mask = 1  # Include home city (index 0)
            for i in subset:
                mask |= (1 << i)
                
            # For each city in the subset, find the best path
            for end in subset:
                # Try all possible previous cities
                min_dist = float('inf')
                min_prev = -1
                
                prev_mask = mask & ~(1 << end)
                for prev in subset:
                    if prev == end:
                        continue
                    
                    curr_dist = dp[prev_mask, prev] + dist_matrix[prev][end]
                    if curr_dist < min_dist:
                        min_dist = curr_dist
                        min_prev = prev
                
                dp[mask, end] = min_dist
                parent[mask, end] = min_prev
    
    # Find the optimal tour
    # Final mask has all cities visited
    final_mask = (1 << n) - 1
    
    # Find the best last city before returning to home
    min_dist = float('inf')
    last_city = -1
    
    for i in range(1, n):
        curr_dist = dp[final_mask, i] + dist_matrix[i][0]  # Distance back to home
        if curr_dist < min_dist:
            min_dist = curr_dist
            last_city = i
            
    # Reconstruct the path
    path = [0]  # Start with home city (index 0)
    mask = final_mask
    curr = last_city
    
    while curr != 0:
        path.append(curr)
        new_curr = parent[mask, curr]
        mask = mask & ~(1 << curr)
        curr = new_curr
        
    path.reverse()
    path.append(0)  # Return to home city
    
    # Convert indices back to city names
    route = [idx_to_city[i] for i in path]
    
    return route, min_dist

def nearest_neighbor(distances, home_city, cities):
    """
    Solve TSP using nearest neighbor heuristic (approximate solution).
    Time complexity: O(n²)
    
    Args:
        distances: Dictionary of distances between cities
        home_city: Starting and ending city
        cities: List of cities to visit
    
    Returns:
        Tuple of (route, total_distance)
    """
    if not cities:
        return [home_city, home_city], 0
    
    cities_to_visit = cities.copy()
    if home_city in cities_to_visit:
        cities_to_visit.remove(home_city)
    
    # Start from home city
    route = [home_city]
    total_distance = 0
    current_city = home_city
    
    # Visit the nearest unvisited city until all are visited
    while cities_to_visit:
        nearest_city = min(cities_to_visit, key=lambda city: distances[current_city][city])
        total_distance += distances[current_city][nearest_city]
        route.append(nearest_city)
        current_city = nearest_city
        cities_to_visit.remove(nearest_city)
    
    # Return to home city
    total_distance += distances[current_city][home_city]
    route.append(home_city)
    
    return route, total_distance
