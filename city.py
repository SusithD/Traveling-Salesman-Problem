class City:
    """Class to represent a city with coordinates."""
    
    def __init__(self, name, x, y):
        """
        Initialize a City object.
        
        Args:
            name: The city name (A to J)
            x, y: Coordinates in a 2D space
        """
        self.name = name
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"City {self.name} ({self.x}, {self.y})"
    
    def distance_to(self, other_city):
        """Calculate Euclidean distance between two cities."""
        return ((self.x - other_city.x) ** 2 + (self.y - other_city.y) ** 2) ** 0.5
