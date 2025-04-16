import unittest
from city import City
from algorithms import brute_force, dynamic_programming, nearest_neighbor

class TestCity(unittest.TestCase):
    
    def test_city_creation(self):
        """Test that a city can be created with the correct attributes."""
        city = City("A", 10, 20)
        self.assertEqual(city.name, "A")
        self.assertEqual(city.x, 10)
        self.assertEqual(city.y, 20)
    
    def test_distance_calculation(self):
        """Test the distance calculation between two cities."""
        city1 = City("A", 0, 0)
        city2 = City("B", 3, 4)
        self.assertEqual(city1.distance_to(city2), 5)  # 3-4-5 triangle

class TestAlgorithms(unittest.TestCase):
    
    def setUp(self):
        """Set up test data for algorithm tests."""
        # Simple distance matrix for testing
        self.distances = {
            'A': {'A': 0, 'B': 10, 'C': 15, 'D': 20},
            'B': {'A': 10, 'B': 0, 'C': 35, 'D': 25},
            'C': {'A': 15, 'C': 0, 'B': 35, 'D': 30},
            'D': {'A': 20, 'B': 25, 'C': 30, 'D': 0}
        }
        self.home_city = 'A'
        self.cities = ['B', 'C', 'D']
    
    def test_brute_force(self):
        """Test the brute force algorithm."""
        route, distance = brute_force(self.distances, self.home_city, self.cities)
        
        # Check route starts and ends at home city
        self.assertEqual(route[0], self.home_city)
        self.assertEqual(route[-1], self.home_city)
        
        # Check all cities are visited
        for city in self.cities:
            self.assertIn(city, route)
    
    def test_dynamic_programming(self):
        """Test the dynamic programming algorithm."""
        route, distance = dynamic_programming(self.distances, self.home_city, self.cities)
        
        # Check route starts and ends at home city
        self.assertEqual(route[0], self.home_city)
        self.assertEqual(route[-1], self.home_city)
        
        # Check all cities are visited
        for city in self.cities:
            self.assertIn(city, route)
    
    def test_nearest_neighbor(self):
        """Test the nearest neighbor algorithm."""
        route, distance = nearest_neighbor(self.distances, self.home_city, self.cities)
        
        # Check route starts and ends at home city
        self.assertEqual(route[0], self.home_city)
        self.assertEqual(route[-1], self.home_city)
        
        # Check all cities are visited
        for city in self.cities:
            self.assertIn(city, route)
    
    def test_empty_cities(self):
        """Test that algorithms handle empty city lists correctly."""
        for algorithm in [brute_force, dynamic_programming, nearest_neighbor]:
            route, distance = algorithm(self.distances, self.home_city, [])
            self.assertEqual(route, [self.home_city, self.home_city])
            self.assertEqual(distance, 0)

if __name__ == '__main__':
    unittest.main()
