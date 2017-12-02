NUM_SIDES = 6

class Current(object):
    def __init__(self, tile, start, end, strength):
        self.path = [start, end]
        self.strength = strength

    def __str__(self):
        return '{start} -> {end} ({strength})'.format(
            start=self.path[0],
            end=self.path[1],
            strength=self.strength)


class Beach(object):
    def __init__(self, tile, num_moorings, *args):
        self.tile = tile
        self.num_moorings = num_moorings
        self.boats = set()
        self.docks = set(args)

    def __str__(self):
        result = ''
        for boat in self.boats:
            result += '[{name}]'.format(name=boat.player.name)
        for i in range(self.num_open_moorings):
            result += '[ ]'

        for dock in self.docks:
            tile_name = '(?)'
            result += '\n{dock} -> {tile_name}'.format(dock=dock, tile_name=tile_name)

        return result

    @property
    def num_open_moorings(self):
        return self.num_moorings - len(self.boats)

    @property
    def is_full(self):
        return self.num_open_moorings == 0

    def count_player_boats(self, player):
        result = 0
        for boat in self.boats:
            if boat and boat.player == player:
                result += 1
        return result

    def place_boat(self, boat):
        assert self.num_open_moorings > 0
        self.boats.add(boat)
        boat.current_beach = self

    def remove_all(self):
        boats = self.boats
        for boat in boats:
            boat.current_beach = None
        self.boats = set()
        return list(boats)


class Tile(object):
    q = None
    r = None
    orientation = 0

    @property
    def is_water(self):
        return type(self) is WaterTile

    @property
    def is_island(self):
        return type(self) is IslandTile


class WaterTile(Tile):
    def __init__(self, currents):
        super().__init__()

        self.name = '(water)'
        self.currents = list(map(lambda args: Current(self, *args), currents))
        self._validate_current_paths()

    def get_end(self, start):
        for current in self.currents:
            if current.path[0] == start:
                return current.path[1]
            if current.path[1] == start:
                return current.path[0]

    def _validate_current_paths(self):
        sides = [side for current in self.currents for side in current.path]
        assert len(sides) == len(set(sides))
        assert len(sides) == NUM_SIDES

    def __str__(self):
        return '(water)\n' + '\n'.join(map(str, self.currents))


class IslandTile(Tile):
    def __init__(self, name, value, beaches):
        super().__init__()

        self.name = name
        self.value = value
        self.beaches = list(map(lambda args: Beach(self, *args), beaches))
        self._validate_beaches()

    def _validate_beaches(self):
        sides = [side for beach in self.beaches for side in beach.docks]
        assert len(sides) == len(set(sides))
        assert len(sides) <= NUM_SIDES

    def __str__(self):
        return '{name} ({value}):\n'.format(name=self.name, value=self.value) + '\n'.join(map(str, self.beaches))

    def count_player_boats(self, player):
        result = 0
        for beach in self.beaches:
            result += beach.count_player_boats(player)
        return result

    @property
    def open_beaches(self):
        return list(filter(lambda beach: beach.num_open_moorings > 0, self.beaches))

