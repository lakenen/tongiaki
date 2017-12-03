"""
Base Tile class
"""

class Tile(object):
    NUM_SIDES = 6

    q = None
    r = None
    orientation = 0

    def __init__(self):
        self.adjacent_tiles = [None] * Tile.NUM_SIDES

    @property
    def is_island(self):
        return False

    @property
    def is_water(self):
        return False
