from tiles.island_tile import IslandTile
from tiles.water_tile import WaterTile
from game import Game
from player import RandomPlayer

def generate_water_tiles():
    return [
        WaterTile('01', [(0, 1, 0), (2, 3, 2), (4, 5, 0)]),
        WaterTile('02', [(0, 1, 2), (2, 3, 0), (4, 5, 2)]),
        WaterTile('03', [(0, 1, 3), (2, 3, 2), (4, 5, 4)]),
        WaterTile('04', [(0, 1, 3), (2, 3, 0), (4, 5, 2)]),

        WaterTile('05', [(0, 3, 4), (1, 5, 3), (2, 4, 0)]),
        WaterTile('06', [(0, 3, 3), (1, 5, 3), (2, 4, 3)]),
        WaterTile('07', [(0, 3, 4), (1, 5, 4), (2, 4, 4)]),
        WaterTile('08', [(0, 3, 3), (1, 5, 2), (2, 4, 0)]),

        WaterTile('09', [(0, 4, 0), (1, 3, 4), (2, 5, 2)]),
        WaterTile('10', [(0, 4, 2), (1, 3, 3), (2, 5, 4)]),
        WaterTile('11', [(0, 4, 4), (1, 3, 4), (2, 5, 3)]),
        WaterTile('12', [(0, 4, 3), (1, 3, 3), (2, 5, 4)]),

        WaterTile('13', [(0, 5, 0), (1, 2, 0), (3, 4, 0)]),
        WaterTile('14', [(0, 5, 2), (1, 2, 2), (3, 4, 2)]),
        WaterTile('15', [(0, 5, 0), (1, 2, 4), (3, 4, 2)]),
        WaterTile('16', [(0, 5, 0), (1, 2, 3), (3, 4, 4)]),
    ]

def generate_island_tiles():
    return [
        IslandTile('Muroroa', 2, [(2, 1), (2, 2), (3, 4, 5)]),
        IslandTile('Nauru', 2, [(2, 1, 2), (3, 3), (2, 4, 5)]),
        IslandTile('Tubuai', 2, [(3, 1, 2), (3, 4, 5)]),

        IslandTile('Rarotonga', 3, [(3, 1, 2), (4, 3, 4, 5)]),
        IslandTile('Rapa Nui', 3, [(5, 1, 2), (3, 3, 4, 5)]),
        IslandTile('Tokelau', 3, [(4, 1), (3, 2, 3), (2, 4, 5)]),
        IslandTile('Tuamotu', 3, [(4, 1, 2, 3), (4, 4, 5)]),

        IslandTile('Hiva Oa', 4, [(2, 1, 2), (2, 3), (5, 4, 5)]),
        IslandTile('Mangareva', 4, [(2, 1, 2), (3, 3, 4), (4, 5)]),
        IslandTile('Oahu', 4, [(3, 1, 2), (5, 3), (3, 4, 5)]),
        IslandTile('Tahiti', 4, [(2, 1, 2), (3, 3, 4), (4, 5)]),
        IslandTile('Tuvalu', 4, [(2, 1, 2), (4, 3), (3, 4, 5)]),

        IslandTile('Fidshi', 5, [(5, 1), (4, 2, 3), (4, 4, 5)]),
        IslandTile('Hawaii', 5, [(3, 1, 2), (5, 3), (2, 4, 5)]),
        IslandTile('Samoa', 5, [(3, 1, 2), (4, 3, 4), (5, 5)]),
    ]

def generate_starting_tile():
    return IslandTile('Tonga', 0, [(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5)])

def generate_tile_stack():
    return generate_water_tiles() + generate_island_tiles()

game = Game(generate_starting_tile(), generate_tile_stack())
game.play([
    RandomPlayer('A'),
    RandomPlayer('B'),
    RandomPlayer('C'),
    RandomPlayer('D'),
    # RandomPlayer('E'),
    # RandomPlayer('F'),
])

# for tile in OFFICIAL_TILES:
#     print(tile)
