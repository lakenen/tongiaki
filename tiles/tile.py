"""
Base Tile class
"""

class Tile(object):
    NUM_SIDES = 6

    q = None
    r = None
    name = '<tile>'
    orientation = 0
    direction = None

    def __init__(self):
        self.adjacent_tiles = [None] * Tile.NUM_SIDES

    @property
    def is_island(self):
        return False

    @property
    def is_water(self):
        return False

    def serialize(self):
        return {
            'q': self.q,
            'r': self.r,
            'name': self.name,
            'orientation': self.orientation,
            'direction': self.direction,
            'adjacent_tiles': [tile.name if tile else None for tile in self.adjacent_tiles]
        }
