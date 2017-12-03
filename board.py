

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
        self.lowest_q = max_q
        self.lowest_r = max_r
        self.highest_q = min_q
        self.highest_r = min_r
        self._grid = [[None] * (self.size_r) for _ in range(self.size_q)]

    def set(self, q, r, obj):
        obj.q = q
        obj.r = r
        q = q - self.min_q
        r = r - self.min_r
        if q < 0 or q >= self.size_q or r < 0 or r >= self.size_r:
            raise Exception("Cannot set a point outside the grid.")
        else:
            self.lowest_q = min(self.lowest_q, q)
            self.lowest_r = min(self.lowest_r, r)
            self.highest_q = max(self.highest_q, q)
            self.highest_r = max(self.highest_r, r)
            self._grid[q][r] = obj

    def get(self, q, r):
        q = q - self.min_q
        r = r - self.min_r
        if q < 0 or q >= self.size_q or r < 0 or r >= self.size_r:
            raise Exception("Cannot get a point outside the grid.")
        else:
            return self._grid[q][r]

    def get_neighbor(self, q, r, direction):
        dq, dr = HexGrid.get_neighbor_offset(direction)
        return self.get(q + dq, r + dr)

    def set_neighbor(self, q, r, direction, obj):
        dq, dr = HexGrid.get_neighbor_offset(direction)
        return self.set(q + dq, r + dr, obj)

    def print(self):
        for q, col in enumerate(self._grid):
            for r, row in enumerate(col):
                if q >= self.lowest_q and r >= self.lowest_r and q <= self.highest_q and r <= self.highest_r:
                    print(q + self.min_q, r + self.min_r, row)



class Board(object):
    def __init__(self, starting_tile):
        self.grid = HexGrid(-8, -8, 8, 8)
        self.grid.set(0, 0, starting_tile)

    def get_neighbor(self, tile, direction):
        return self.grid.get_neighbor(tile.q, tile.r,  direction - tile.orientation)

    def set_neighbor(self, tile, direction, new_tile):
        direction = (direction - tile.orientation) % 6
        if direction == 0:
            new_tile.orientation = 3
        elif direction == 1:
            new_tile.orientation = 2
        elif direction == 2:
            new_tile.orientation = 1
        elif direction == 3:
            new_tile.orientation = 0
        elif direction == 4:
            new_tile.orientation = 5
        elif direction == 5:
            new_tile.orientation = 4
        else:
            print('BAD DIRECTIONSSSSS')
        return self.grid.set_neighbor(tile.q, tile.r, direction, new_tile)

    def print(self):
        self.grid.print()
