from tiles.tile import Tile


class Beach(object):
    def __init__(self, tile, num_moorings, *args):
        self.tile = tile
        self.num_moorings = num_moorings
        self.boats = set()
        self.docks = set(args) # called 'footbriges' in the official rules

    def __str__(self):
        result = '|'
        for boat in self.boats:
            result += '{name}|'.format(name=boat.player.name)
        for i in range(self.num_open_moorings):
            result += '_|'

        # for dock in self.docks:
        #     tile_name = '(?)'
        #     result += '\n{dock} -> {tile_name}'.format(dock=dock, tile_name=tile_name)
        result += ' ' + ','.join(map(str, self.docks))

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

    def serialize(self):
        moorings = [boat.player.name for boat in self.boats] + [None] * (self.num_moorings - len(self.boats))
        return {
            'moorings': moorings,
            'footbridges': list(self.docks)
        }


class IslandTile(Tile):
    def __init__(self, name, value, beaches):
        super().__init__()

        self.name = name
        self.value = value
        self.beaches = list(map(lambda args: Beach(self, *args), beaches))
        self._validate_beaches()

    @property
    def is_island(self):
        return True

    def _validate_beaches(self):
        sides = [side for beach in self.beaches for side in beach.docks]
        assert len(sides) == len(set(sides))
        assert len(sides) <= Tile.NUM_SIDES

    def __str__(self):
        return '{name} ({value}) ({q},{r}/{o}):\n'.format(
            q=self.q,
            r=self.r,
            o=self.orientation,
            name=self.name,
            value=self.value) + '\n'.join(map(str, self.beaches))

    def count_player_boats(self, player):
        result = 0
        for beach in self.beaches:
            result += beach.count_player_boats(player)
        return result

    @property
    def open_beaches(self):
        return list(filter(lambda beach: beach.num_open_moorings > 0, self.beaches))

    def serialize(self):
        result = super().serialize()
        result['value'] = self.value
        result['beaches'] = list(map(lambda beach: beach.serialize(), self.beaches))
        return result
