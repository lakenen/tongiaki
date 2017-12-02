NUM_SIDES = 6

class Current(object):
    def __init__(self, start, end, strength):
        self.path = [start, end]
        self.strength = strength

    def __str__(self):
        return '{start} -> {end} ({strength})'.format(
            start=self.path[0],
            end=self.path[1],
            strength=self.strength)


class Beach(object):
    def __init__(self, num_moorings, *args):
        self.moorings = [None] * num_moorings
        self.docks = set(args)

    def __str__(self):
        return '[]'.join(['' for i in self.moorings]) + '\n' + ', '.join(map(str,self.docks))


class Tile(object):
    def __init__(self):
        self.adjacent_tiles = [None] * NUM_SIDES


class WaterTile(Tile):
    def __init__(self, currents):
        super().__init__()

        self.currents = currents
        self._validate_current_paths()

    def _validate_current_paths(self):
        sides = [side for current in self.currents for side in current.path]
        assert len(sides) == len(set(sides))
        assert len(sides) == NUM_SIDES

    def __str__(self):
        return 'Water:\n' + '\n'.join(map(str, self.currents))


class IslandTile(Tile):
    def __init__(self, name, value, beaches):
        super().__init__()

        self.name = name
        self.value = value
        self.beaches = beaches
        self._validate_beaches()

    def _validate_beaches(self):
        sides = [side for beach in self.beaches for side in beach.docks]
        assert len(sides) == len(set(sides))
        assert len(sides) <= NUM_SIDES

    def __str__(self):
        return '{name} ({value}):\n'.format(name=self.name, value=self.value) + '\n'.join(map(str, self.beaches))
