"""
File:          Coordinates.py
Date:          February 2024
Description:   This file contains a structure for organizing two-dimensional coordinates (x and y).
Author:        Nordine HIDA
Modifications:
"""


class Coordinates:
    """
    Structure representing coordinates.
    """

    def __init__(self, x, y):
        """
        Initialize coordinates with x and y values.
        :param x: X coordinate
        :param y: Y coordinate
        """
        self.x = x
        self.y = y
