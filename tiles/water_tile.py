from tiles.tile import Tile


class Current(object):
    def __init__(self, tile, start, end, strength):
        self.path = [start, end]
        self.strength = strength

    def __str__(self):
        return '{start} -> {end} ({strength})'.format(
            start=self.path[0],
            end=self.path[1],
            strength=self.strength)


class WaterTile(Tile):
    def __init__(self, currents):
        super().__init__()

        self.name = '(water)'
        self.currents = list(map(lambda args: Current(self, *args), currents))
        self._validate_current_paths()

    @property
    def is_water(self):
        return True

    def get_end(self, start):
        for current in self.currents:
            if current.path[0] == start:
                return current.path[1]
            if current.path[1] == start:
                return current.path[0]

    def can_pass(self, boats, start):
        num_players = len(set(map(lambda boat: boat.player, boats)))
        for current in self.currents:
            if start in current.path:
                return num_players >= current.strength
        return False

    def _validate_current_paths(self):
        sides = [side for current in self.currents for side in current.path]
        assert len(sides) == len(set(sides))
        assert len(sides) == Tile.NUM_SIDES

    def __str__(self):
        return '(water)\n' + '\n'.join(map(str, self.currents))
