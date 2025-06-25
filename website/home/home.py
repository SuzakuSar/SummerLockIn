"""
Enhanced Space-themed Homepage Blueprint for SUMMERLOCKIN Project
Uses advanced constellation patterns and complex nebula effects
"""

from flask import Blueprint, render_template, jsonify
import random
import math
import json

# Import the space effects module
# Note: You'll need to place space_effects.py in the website folder
try:
    from ..space_effects import ConstellationGenerator, NebulaGenerator, SpaceEffects
except ImportError:
    # Fallback if space_effects isn't available yet
    from website.space_effects import ConstellationGenerator, NebulaGenerator, SpaceEffects

# Create blueprint with template folder
home = Blueprint('home', __name__, template_folder='templates')

def generate_enhanced_constellation():
    """
    Generate an enhanced constellation using Poisson disk sampling
    for natural star distribution
    """
    # Use Poisson disk sampling for realistic star distribution
    generator = ConstellationGenerator()
    
    # Generate stars with natural spacing
    # Min distance prevents clustering
    stars = generator.poisson_disk_sampling(
        width=95,  # Keep 5% margin
        height=90,  # Keep 10% margin for header
        min_distance=12,  # Minimum distance between stars
        num_samples=30
    )
    
    # Limit star count for performance
    if len(stars) > 25:
        stars = random.sample(stars, 25)
    
    # Generate constellation lines
    lines = generator.generate_constellation_lines(
        stars=stars,
        max_distance=35,  # Maximum line length
        connectivity=0.4  # 40% chance of connection
    )
    
    return {
        'stars': stars,
        'lines': lines,
        'metadata': {
            'star_count': len(stars),
            'line_count': len(lines),
            'generation_method': 'poisson_disk'
        }
    }

def generate_enhanced_nebulae():
    """
    Generate complex, multi-layered nebulae for rich background
    """
    generator = NebulaGenerator()
    
    # Generate 3-6 nebulae for variety
    num_nebulae = random.randint(3, 6)
    nebulae = generator.generate_nebula_field(count=num_nebulae)
    
    return nebulae

def generate_dynamic_effects():
    """
    Generate parameters for dynamic effects like shooting stars
    """
    effects = SpaceEffects()
    
    return {
        'shooting_stars': {
            'enabled': True,
            'frequency': random.uniform(0.3, 0.5),  # 30-50% chance per interval
            'interval': random.randint(2000, 4000),  # Check every 2-4 seconds
            'params': [effects.generate_shooting_star_params() for _ in range(5)]
        },
        'pulsars': {
            'enabled': True,
            'count': random.randint(2, 4),
            'positions': [
                {
                    'x': random.uniform(10, 90),
                    'y': random.uniform(10, 90),
                    'period': random.uniform(1, 3),
                    'size': random.randint(15, 30)
                } for _ in range(random.randint(2, 4))
            ]
        },
        'cosmic_dust': {
            'enabled': True,
            'particle_count': 100,
            'drift_speed': random.uniform(0.5, 1.5)
        }
    }

@home.route('/')
def index():
    """
    Main homepage route - renders space-themed navigation hub
    """
    # Generate all space effects data
    constellation = generate_enhanced_constellation()
    nebulae = generate_enhanced_nebulae()
    effects = generate_dynamic_effects()
    
    # Add some statistics for display
    stats = {
        'total_stars': constellation['metadata']['star_count'],
        'total_connections': constellation['metadata']['line_count'],
        'nebula_count': len(nebulae),
        'brightest_star': max(constellation['stars'], key=lambda s: s['brightness'])
    }
    
    return render_template('home.html.jinja2',
                         constellation=constellation,
                         nebulae=nebulae,
                         effects=effects,
                         stats=stats)

@home.route('/api/constellation/new')
def new_constellation():
    """
    API endpoint for generating new constellation patterns
    """
    constellation = generate_enhanced_constellation()
    return jsonify(constellation)

@home.route('/api/nebulae/new')
def new_nebulae():
    """
    API endpoint for generating new nebula patterns
    """
    nebulae = generate_enhanced_nebulae()
    return jsonify(nebulae)

@home.route('/api/effects/shooting-star')
def new_shooting_star():
    """
    API endpoint for generating new shooting star parameters
    """
    effects = SpaceEffects()
    return jsonify(effects.generate_shooting_star_params())

@home.route('/api/space/full-regenerate')
def full_space_regenerate():
    """
    API endpoint to regenerate all space elements at once
    """
    return jsonify({
        'constellation': generate_enhanced_constellation(),
        'nebulae': generate_enhanced_nebulae(),
        'effects': generate_dynamic_effects(),
        'timestamp': random.randint(1000000, 9999999)  # For cache busting
    })