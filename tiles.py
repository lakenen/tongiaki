
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
    moorings = []

    def __init__(self, num_moorings, *args):
        self.num_moorings = num_moorings
        self.docks = set(args)

    def __str__(self):
        return '[]'.join(['' for i in range(0, self.num_moorings + 1)]) + '\n' + ', '.join(map(str,self.docks))


class Tile(object):
    pass


class WaterTile(Tile):
    def __init__(self, currents):
        super().__init__()

        self.currents = currents
        self._validate_current_paths()

    def _validate_current_paths(self):
        sides = [side for current in self.currents for side in current.path]
        assert len(sides) == len(set(sides))

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

    def __str__(self):
        return '{name} ({value}):\n'.format(name=self.name, value=self.value) + '\n'.join(map(str, self.beaches))



OFFICIAL_TILES = [
    WaterTile([Current(0, 1, 0), Current(2, 3, 2), Current(4, 5, 0)]),
    WaterTile([Current(0, 1, 2), Current(2, 3, 0), Current(4, 5, 2)]),
    WaterTile([Current(0, 1, 3), Current(2, 3, 2), Current(4, 5, 4)]),
    WaterTile([Current(0, 1, 3), Current(2, 3, 0), Current(4, 5, 2)]),

    WaterTile([Current(0, 3, 4), Current(1, 5, 3), Current(2, 4, 0)]),
    WaterTile([Current(0, 3, 3), Current(1, 5, 3), Current(2, 4, 3)]),
    WaterTile([Current(0, 3, 4), Current(1, 5, 4), Current(2, 4, 4)]),
    WaterTile([Current(0, 3, 3), Current(1, 5, 2), Current(2, 4, 0)]),

    WaterTile([Current(0, 4, 0), Current(1, 3, 4), Current(2, 5, 2)]),
    WaterTile([Current(0, 4, 2), Current(1, 3, 3), Current(2, 5, 4)]),
    WaterTile([Current(0, 4, 4), Current(1, 3, 4), Current(2, 5, 3)]),
    WaterTile([Current(0, 4, 3), Current(1, 3, 3), Current(2, 5, 4)]),

    WaterTile([Current(0, 5, 0), Current(1, 2, 0), Current(3, 4, 0)]),
    WaterTile([Current(0, 5, 2), Current(1, 2, 2), Current(3, 4, 2)]),
    WaterTile([Current(0, 5, 0), Current(1, 2, 4), Current(3, 4, 2)]),
    WaterTile([Current(0, 5, 0), Current(1, 2, 3), Current(3, 4, 4)]),

    IslandTile('Tonga', 0, [Beach(3, 0), Beach(3, 1), Beach(3, 2), Beach(3, 3), Beach(3, 4), Beach(3, 5)]),
    IslandTile('Muroroa', 2, [Beach(2, 1), Beach(2, 2), Beach(3, 4, 5)]),
    IslandTile('Nauru', 2, [Beach(2, 1, 2), Beach(3, 3), Beach(2, 4, 5)]),
    IslandTile('Tubuai', 2, [Beach(3, 1, 2), Beach(3, 4, 5)]),

    IslandTile('Rarotonga', 3, [Beach(3, 1, 2), Beach(4, 3, 4, 5)]),
    IslandTile('Rapa Nui', 3, [Beach(5, 1, 2), Beach(3, 3, 4, 5)]),
    IslandTile('Tokelau', 3, [Beach(4, 1), Beach(3, 2, 3), Beach(2, 4, 5)]),
    IslandTile('Tuamotu', 3, [Beach(4, 1, 2, 3), Beach(4, 4, 5)]),

    IslandTile('Hiva Oa', 4, [Beach(2, 1, 2), Beach(2, 3), Beach(5, 4, 5)]),
    IslandTile('Mangareva', 4, [Beach(2, 1, 2), Beach(3, 3, 4), Beach(4, 5)]),
    IslandTile('Oahu', 4, [Beach(3, 1, 2), Beach(5, 3), Beach(3, 4, 5)]),
    IslandTile('Tahiti', 4, [Beach(2, 1, 2), Beach(3, 3, 4), Beach(4, 5)]),
    IslandTile('Tuvalu', 4, [Beach(2, 1, 2), Beach(4, 3), Beach(3, 4, 5)]),

    IslandTile('Fidshi', 5, [Beach(5, 1), Beach(4, 2, 3), Beach(4, 4, 5)]),
    IslandTile('Hawaii', 5, [Beach(3, 1, 2), Beach(5, 3), Beach(2, 4, 5)]),
    IslandTile('Samoa', 5, [Beach(3, 1, 2), Beach(4, 3, 4), Beach(5, 5)]),
]

for tile in OFFICIAL_TILES:
    print(tile)
