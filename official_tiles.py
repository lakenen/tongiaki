from random import shuffle
from tiles import Beach, Current, IslandTile, WaterTile
from game import Game

def generate_water_tiles():
    return [
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
    ]

def generate_island_tiles():
    return [
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

def generate_starting_tile()
    return IslandTile('Tonga', 0, [Beach(3, 0), Beach(3, 1), Beach(3, 2), Beach(3, 3), Beach(3, 4), Beach(3, 5)])

def generate_tile_stack():
    return shuffle(generate_water_tiles() + generate_island_tiles())

game = Game(generate_starting_tile(), generate_tile_stack())

# for tile in OFFICIAL_TILES:
#     print(tile)
