"""
Ontological Recursion Framework
===============================
A framework for modeling reality as a self-referential system where consciousness 
participates in creating the conditions of its own emergence.

Compatible with Process Metaphysics, Morphogenesis, and Schizoanalytic thinking,
with QBism as a meta-framework.
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from scipy.spatial import distance
from scipy import signal
import seaborn as sns
import random
from IPython.display import clear_output
import time
import pandas as pd


class ActualOccasion:
    """
    Represents Whitehead's concept of an actual occasion - a basic unit
    of process reality that comes into being, reaches satisfaction, and perishes.
    """
    def __init__(self, id, intensity=1.0, position=None):
        self.id = id
        self.intensity = intensity  # Intensity of experience/feeling
        self.prehensions = []  # Connections to other occasions
        self.position = position if position is not None else np.random.rand(2)  # Spatial position for visualization
        self.satisfaction = 0.0  # Degree of completion
        self.perished = False
        self.data = {}  # Container for emergence properties
        
    def prehend(self, other, strength):
        """Create a prehension (feeling) of another occasion"""
        self.prehensions.append((other, strength))
        return self
    
    def update(self, dt):
        """Process toward satisfaction"""
        if self.perished:
            return
            
        # Increase satisfaction based on intensity and prehensions
        prehension_factor = sum(strength for _, strength in self.prehensions)
        self.satisfaction += dt * self.intensity * (1 + 0.1 * prehension_factor)
        
        if self.satisfaction >= 1.0:
            self.perish()
            
    def perish(self):
        """Occasion reaches completion and perishes"""
        self.perished = True
        self.satisfaction = 1.0


class ProcessLevel:
    """
    Represents the level of process metaphysics where actual occasions
    form societies and create emergent patterns.
    """
    def __init__(self):
        self.occasions = []
        self.next_id = 0
        self.historic_occasions = []  # Archive of perished occasions
        
    def create_occasion(self, intensity=None, position=None):
        """Generate a new actual occasion"""
        if intensity is None:
            intensity = random.uniform(0.5, 1.5)
            
        occasion = ActualOccasion(self.next_id, intensity, position)
        self.occasions.append(occasion)
        self.next_id += 1
        return occasion
        
    def create_society(self, num_occasions, connection_density=0.3):
        """
        Create a society of interconnected occasions.

        Parameters:
            num_occasions (int): Number of occasions to create.
            connection_density (float): Probability of connections between occasions (0 to 1).

        Returns:
            list: List of created occasions.
        """
        new_occasions = [self.create_occasion() for _ in range(num_occasions)]
        
        # Create prehensions between occasions
        for i, occasion in enumerate(new_occasions):
            for j, other in enumerate(new_occasions):
                if i != j and random.random() < connection_density:
                    strength = random.uniform(0.1, 0.9)
                    occasion.prehend(other, strength)
                    
        return new_occasions
    
    def update(self, dt):
        """Update all occasions"""
        # Update existing occasions
        for occasion in self.occasions:
            occasion.update(dt)
            
        # Move perished occasions to historic archive
        active_occasions = []
        for occasion in self.occasions:
            if occasion.perished:
                self.historic_occasions.append(occasion)
            else:
                active_occasions.append(occasion)
                
        self.occasions = active_occasions
        
    def create_occasion_from_pattern(self):
        """Create new occasions that resonate with past patterns"""
        
        if not self.historic_occasions: 
            return None 
        
