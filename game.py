from tiles import IslandTile, WaterTile
from random import shuffle

class GameOver(Exception):
    pass

class HexGrid(object):
    @classmethod
    def get_neighbor_offset(cls, direction):
        direction = direction % 6
        # down == 0 -> 0, 1
        if direction == 0:
            return 0, 1
        # down-left == 1 -> -1, 1
        if direction == 1:
            return -1, 1
        # up-left == 2 -> -1, 0
        if direction == 2:
            return -1, 0
        # up == 3 -> 0, -1
        if direction == 3:
            return 0, -1
        # up-right == 4 -> 1, -1
        if direction == 4:
            return 1, -1
        # down-right == 5 -> 1, 0
        if direction == 5:
            return 1, 0

    def __init__(self, min_q, min_r, max_q, max_r):
        self.min_q = min_q
        self.min_r = min_r
        self.max_q = max_q
        self.max_r = max_r
        self.size_q = max_q - min_q + 1
        self.size_r = max_r - min_r + 1
        self._grid = [[None] * (self.size_r) for _ in range(self.size_q)]

    def set(self, q, r, obj):
        obj.q = q
        obj.r = r
        q = q - self.min_q
        r = r - self.min_r
        if q < 0 or q >= self.size_q or r < 0 or r >= self.size_r:
            print( self._grid)
            raise Exception("Cannot set a point outside the grid.")
        else:
            self._grid[q][r] = obj

    def get(self, q, r):
        q = q - self.min_q
        r = r - self.min_r
        if q < 0 or q >= self.size_q or r < 0 or r >= self.size_r:
            print( self._grid)
            raise Exception("Cannot get a point outside the grid.")
        else:
            return self._grid[q][r]

    def get_neighbor(self, q, r, direction):
        dq, dr = HexGrid.get_neighbor_offset(direction)
        return self.get(q + dq, r + dr)

    def set_neighbor(self, q, r, direction, obj):
        print('set', q, r)
        dq, dr = HexGrid.get_neighbor_offset(direction)
        return self.set(q + dq, r + dr, obj)


class Board(object):
    def __init__(self, starting_tile):
        self.grid = HexGrid(-16, -16, 16, 16)
        self.grid.set(0, 0, starting_tile)

    def get_neighbor(self, tile, direction):
        return self.grid.get_neighbor(tile.q, tile.r,  direction - tile.orientation)

    def set_neighbor(self, tile, direction, new_tile):
        return self.grid.set_neighbor(tile.q, tile.r,  direction - tile.orientation, new_tile)

class Game(object):
    def __init__(self, starting_tile, tile_stack, num_initial_boats=2):

        shuffle(tile_stack)
        self.tile_stack = tile_stack
        # for tile in self.tile_stack:
        #     print(tile, '\n')

        self.starting_tile = starting_tile
        self.island_tiles = set([starting_tile])
        self.water_tiles = set()
        self.num_initial_boats = num_initial_boats
        self.board = Board(self.starting_tile)

    def get_tile(self):
        tile = self.tile_stack.pop(0)
        if tile.is_island:
            self.island_tiles.add(tile)
        elif tile.is_water:
            self.water_tiles.add(tile)
            # End immediately if the last tile is a water
            if self.is_over:
                raise GameOver()

        return tile

    @property
    def is_over(self):
        remaining_islands = list(filter(lambda tile: tile.is_island, self.tile_stack))
        remaining_waters = list(filter(lambda tile: tile.is_water, self.tile_stack))
        return remaining_islands == 0 or remaining_waters == 0

    def setup(self):
        for i in range(self.num_initial_boats):
            for player in self.players:
                player.place_initial_boat(self.starting_tile)

    def resolve_migrations(self, player):
        while True:
            beach = player.choose_beach_to_migrate()
            if not beach:
                return
            direction = player.choose_dock(beach)
            current_tile = beach.tile
            current_boats = beach.remove_all()
            while True:
                if self.is_over:
                    raise GameOver()

                next_tile = self.board.get_neighbor(current_tile, direction)
                if next_tile:
                    # TODO: determine starting direction
                    print(next_tile)
                else:
                    next_tile = self.get_tile()
                    if direction < 3:
                        next_tile.orientation = direction - 3
                    elif direction == 3:
                        next_tile.orientation = 0
                    else:
                        next_tile.orientation = 6 - (direction - 3)

                    self.board.set_neighbor(current_tile, direction, next_tile)

                    # starting direction is always 0 for new tiles
                    direction = 0

                current_tile = next_tile

                if current_tile.is_water:
                    direction = current_tile.get_end(direction)
                    continue
                elif current_tile.is_island:
                    # landfall!
                    player.place_boats(current_tile, current_boats)
                    break

    def play_turn(self, player):
        island_to_expand = player.choose_island_to_expand()
        player.expand(island_to_expand)
        self.resolve_migrations(player)

    def play(self, players):
        # assume players are passed in in the order they'll play in
        self.players = players
        self.setup()
        print(self.starting_tile,'\n')

        try:
            while True:
                for player in self.players:
                    self.play_turn(player)
        except GameOver:
            print('game over!')

        for tile in self.island_tiles:
            print(tile,'\n')
