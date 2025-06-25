"""
Space Effects Module for SUMMERLOCKIN Project
Provides reusable generators for constellation patterns, nebula clouds, and other space effects
"""

import random
import math
from typing import List, Dict, Tuple, Optional
import colorsys

class ConstellationGenerator:
    """
    Advanced constellation generator with realistic star distributions
    and natural-looking connection patterns
    """
    
    @staticmethod
    def poisson_disk_sampling(width: int, height: int, min_distance: float, num_samples: int = 30) -> List[Dict]:
        """
        Generate stars using Poisson disk sampling for natural distribution
        Prevents stars from clustering too close together
        
        Args:
            width: Canvas width percentage (usually 100)
            height: Canvas height percentage (usually 100)
            min_distance: Minimum distance between stars
            num_samples: Number of attempts to place each star
            
        Returns:
            List of star positions with properties
        """
        cell_size = min_distance / math.sqrt(2)
        grid_width = int(width / cell_size) + 1
        grid_height = int(height / cell_size) + 1
        
        # Initialize grid
        grid = [[None for _ in range(grid_height)] for _ in range(grid_width)]
        active_list = []
        stars = []
        
        # Add first random point
        first_point = {
            'x': random.uniform(10, width - 10),
            'y': random.uniform(10, height - 10)
        }
        active_list.append(first_point)
        
        grid_x = int(first_point['x'] / cell_size)
        grid_y = int(first_point['y'] / cell_size)
        grid[grid_x][grid_y] = first_point
        
        while active_list:
            # Pick random point from active list
            idx = random.randint(0, len(active_list) - 1)
            point = active_list[idx]
            found = False
            
            # Try to generate new points around it
            for _ in range(num_samples):
                # Generate random point in annulus
                angle = random.uniform(0, 2 * math.pi)
                radius = random.uniform(min_distance, min_distance * 2)
                
                new_x = point['x'] + radius * math.cos(angle)
                new_y = point['y'] + radius * math.sin(angle)
                
                # Check if within bounds
                if new_x < 5 or new_x > width - 5 or new_y < 5 or new_y > height - 5:
                    continue
                
                # Check grid neighbors
                grid_x = int(new_x / cell_size)
                grid_y = int(new_y / cell_size)
                
                # Check neighboring cells
                neighbors_clear = True
                for dx in range(-2, 3):
                    for dy in range(-2, 3):
                        nx, ny = grid_x + dx, grid_y + dy
                        if 0 <= nx < grid_width and 0 <= ny < grid_height:
                            neighbor = grid[nx][ny]
                            if neighbor:
                                dist = math.sqrt((new_x - neighbor['x'])**2 + (new_y - neighbor['y'])**2)
                                if dist < min_distance:
                                    neighbors_clear = False
                                    break
                    if not neighbors_clear:
                        break
                
                if neighbors_clear:
                    new_point = {'x': new_x, 'y': new_y}
                    active_list.append(new_point)
                    grid[grid_x][grid_y] = new_point
                    stars.append(new_point)
                    found = True
                    break
            
            if not found:
                active_list.pop(idx)
        
        # Add first point to stars
        stars.insert(0, first_point)
        
        # Enhance stars with additional properties
        for i, star in enumerate(stars):
            star['id'] = i
            # Vary star sizes based on "magnitude"
            magnitude = random.random()
            if magnitude > 0.95:  # Bright stars (5%)
                star['size'] = random.randint(8, 12)
                star['brightness'] = random.uniform(0.9, 1.0)
                star['twinkle_speed'] = random.uniform(2, 4)
            elif magnitude > 0.8:  # Medium stars (15%)
                star['size'] = random.randint(5, 8)
                star['brightness'] = random.uniform(0.7, 0.9)
                star['twinkle_speed'] = random.uniform(3, 5)
            else:  # Dim stars (80%)
                star['size'] = random.randint(2, 5)
                star['brightness'] = random.uniform(0.4, 0.7)
                star['twinkle_speed'] = random.uniform(4, 8)
            
            # Animation properties
            star['animation_delay'] = random.uniform(0, 10)
            star['animation_duration'] = star['twinkle_speed']
            star['pulse_offset'] = random.uniform(0, 2 * math.pi)
            
            # Color variation (slight tint)
            star['color_temp'] = random.choice(['warm', 'neutral', 'cool'])
            
        return stars
    
    @staticmethod
    def generate_constellation_lines(stars: List[Dict], max_distance: float = 30, 
                                   connectivity: float = 0.3) -> List[Dict]:
        """
        Generate constellation lines using Delaunay triangulation with filtering
        
        Args:
            stars: List of star dictionaries with x, y coordinates
            max_distance: Maximum distance for line connections
            connectivity: Probability of keeping a connection (0-1)
            
        Returns:
            List of line dictionaries
        """
        lines = []
        star_count = len(stars)
        
        # Create adjacency tracking to avoid duplicate lines
        connections = set()
        
        # For each star, connect to nearby stars
        for i in range(star_count):
            star1 = stars[i]
            
            # Find potential connections
            potential_connections = []
            
            for j in range(i + 1, star_count):
                star2 = stars[j]
                
                # Calculate distance
                dx = star2['x'] - star1['x']
                dy = star2['y'] - star1['y']
                distance = math.sqrt(dx**2 + dy**2)
                
                if distance <= max_distance:
                    potential_connections.append((j, distance, dx, dy))
            
            # Sort by distance
            potential_connections.sort(key=lambda x: x[1])
            
            # Connect to nearest stars based on connectivity
            max_connections = random.randint(1, 3)  # Each star connects to 1-3 others
            connections_made = 0
            
            for j, distance, dx, dy in potential_connections:
                if connections_made >= max_connections:
                    break
                
                # Check if connection already exists
                connection_key = (min(i, j), max(i, j))
                if connection_key in connections:
                    continue
                
                # Probability of connection decreases with distance
                connection_prob = connectivity * (1 - distance / max_distance)
                
                if random.random() < connection_prob:
                    connections.add(connection_key)
                    connections_made += 1
                    
                    # Calculate angle for line rotation
                    angle = math.degrees(math.atan2(dy, dx))
                    
                    line = {
                        'star1_id': i,
                        'star2_id': j,
                        'x1': star1['x'],
                        'y1': star1['y'],
                        'x2': star2['x'],
                        'y2': star2['y'],
                        'length': distance,
                        'angle': angle,
                        'brightness': min(star1['brightness'], star2['brightness']) * 0.6,
                        'animation_delay': random.uniform(0, 5),
                        'animation_duration': random.uniform(4, 8),
                        'pulse_speed': random.uniform(0.5, 2)
                    }
                    lines.append(line)
        
        return lines

class NebulaGenerator:
    """
    Advanced nebula generator creating complex, layered cloud effects
    """
    
    @staticmethod
    def generate_complex_nebula() -> Dict:
        """
        Generate a complex nebula with multiple layers and color variations
        
        Returns:
            Dictionary containing nebula properties
        """
        # Base nebula properties
        nebula = {
            'x': random.uniform(0, 100),
            'y': random.uniform(0, 100),
            'layers': []
        }
        
        # Color schemes for different nebula types
        nebula_types = [
            {  # Emission nebula (pink/red)
                'name': 'emission',
                'colors': [
                    'rgba(255, 20, 147, {alpha})',   # Deep pink
                    'rgba(220, 20, 60, {alpha})',    # Crimson
                    'rgba(255, 105, 180, {alpha})'   # Hot pink
                ]
            },
            {  # Reflection nebula (blue)
                'name': 'reflection',
                'colors': [
                    'rgba(0, 191, 255, {alpha})',    # Deep sky blue
                    'rgba(30, 144, 255, {alpha})',   # Dodger blue
                    'rgba(135, 206, 250, {alpha})'   # Light sky blue
                ]
            },
            {  # Planetary nebula (green/teal)
                'name': 'planetary',
                'colors': [
                    'rgba(0, 255, 127, {alpha})',    # Spring green
                    'rgba(64, 224, 208, {alpha})',   # Turquoise
                    'rgba(0, 206, 209, {alpha})'     # Dark turquoise
                ]
            },
            {  # Dark nebula (purple/violet)
                'name': 'dark',
                'colors': [
                    'rgba(138, 43, 226, {alpha})',   # Blue violet
                    'rgba(75, 0, 130, {alpha})',     # Indigo
                    'rgba(128, 0, 128, {alpha})'     # Purple
                ]
            }
        ]
        
        # Choose nebula type
        nebula_type = random.choice(nebula_types)
        nebula['type'] = nebula_type['name']
        
        # Generate 3-5 layers for complexity
        num_layers = random.randint(3, 5)
        
        for i in range(num_layers):
            # Each layer has different properties
            layer_size = random.randint(200, 600) * (1 + i * 0.3)  # Outer layers larger
            layer_alpha = random.uniform(0.1, 0.4) / (i + 1)  # Outer layers more transparent
            
            # Offset each layer slightly
            offset_x = random.uniform(-20, 20)
            offset_y = random.uniform(-20, 20)
            
            # Choose color from palette
            color_template = random.choice(nebula_type['colors'])
            color = color_template.format(alpha=layer_alpha)
            
            # Create gradient type
            gradient_types = [
                f'radial-gradient(circle at {random.randint(30, 70)}% {random.randint(30, 70)}%, {color}, transparent {random.randint(40, 70)}%)',
                f'radial-gradient(ellipse at {random.randint(20, 80)}% {random.randint(20, 80)}%, {color}, transparent {random.randint(50, 80)}%)',
                f'conic-gradient(from {random.randint(0, 360)}deg at {random.randint(40, 60)}% {random.randint(40, 60)}%, {color}, transparent, {color})'
            ]
            
            layer = {
                'size': layer_size,
                'offset_x': offset_x,
                'offset_y': offset_y,
                'gradient': random.choice(gradient_types),
                'blur': random.randint(40, 100),
                'opacity': layer_alpha,
                'animation_duration': random.uniform(20, 40),
                'animation_delay': random.uniform(0, 10),
                'rotation_speed': random.uniform(-30, 30)  # Degrees per cycle
            }
            
            nebula['layers'].append(layer)
        
        # Add some bright spots for detail
        nebula['bright_spots'] = []
        for _ in range(random.randint(2, 5)):
            spot = {
                'offset_x': random.uniform(-30, 30),
                'offset_y': random.uniform(-30, 30),
                'size': random.randint(20, 60),
                'brightness': random.uniform(0.5, 1.0),
                'color': 'rgba(255, 255, 255, {alpha})'.format(alpha=random.uniform(0.3, 0.7))
            }
            nebula['bright_spots'].append(spot)
        
        return nebula
    
    @staticmethod
    def generate_nebula_field(count: int = 5) -> List[Dict]:
        """
        Generate multiple nebulae for a rich background
        
        Args:
            count: Number of nebulae to generate
            
        Returns:
            List of nebula dictionaries
        """
        nebulae = []
        
        # Ensure variety in positioning
        quadrants = [(0, 50, 0, 50), (50, 100, 0, 50), 
                     (0, 50, 50, 100), (50, 100, 50, 100)]
        
        for i in range(count):
            nebula = NebulaGenerator.generate_complex_nebula()
            
            # Distribute across quadrants for better coverage
            if i < len(quadrants):
                x_min, x_max, y_min, y_max = quadrants[i]
                nebula['x'] = random.uniform(x_min, x_max)
                nebula['y'] = random.uniform(y_min, y_max)
            
            nebulae.append(nebula)
        
        return nebulae

class SpaceEffects:
    """
    Additional space effects like shooting stars, galaxies, etc.
    """
    
    @staticmethod
    def generate_shooting_star_params() -> Dict:
        """Generate parameters for shooting star effects"""
        return {
            'start_x': random.choice([-200, 100]),  # Start from left or right
            'start_y': random.uniform(0, 50),
            'end_x_offset': random.uniform(300, 600),
            'end_y_offset': random.uniform(100, 300),
            'duration': random.uniform(2, 4),
            'delay': random.uniform(0, 10),
            'size': random.randint(2, 4),
            'tail_length': random.randint(50, 150)
        }
    
    @staticmethod
    def generate_galaxy_spiral(center_x: float, center_y: float, arms: int = 2) -> List[Dict]:
        """
        Generate points for a spiral galaxy pattern
        
        Args:
            center_x: X coordinate of galaxy center
            center_y: Y coordinate of galaxy center
            arms: Number of spiral arms
            
        Returns:
            List of points forming spiral arms
        """
        points = []
        points_per_arm = 50
        
        for arm in range(arms):
            arm_offset = (2 * math.pi / arms) * arm
            
            for i in range(points_per_arm):
                # Logarithmic spiral
                angle = (i / points_per_arm) * 4 * math.pi + arm_offset
                radius = 5 * math.exp(0.1 * angle)
                
                # Add some randomness
                radius += random.uniform(-2, 2)
                angle += random.uniform(-0.1, 0.1)
                
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                
                # Only include if within bounds
                if 0 <= x <= 100 and 0 <= y <= 100:
                    points.append({
                        'x': x,
                        'y': y,
                        'size': random.uniform(1, 3),
                        'brightness': random.uniform(0.3, 0.8) * (1 - i / points_per_arm)
                    })
        
        return points