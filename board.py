

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
        num_tiles_to_print = len(list(filter(bool,[a for b in self._grid for a in b])))
        tiles_found = 0
        alternate = 0
        lines = []

        print('low', self.lowest_q + self.min_q, self.lowest_r + self.min_r)
        print('high', self.highest_q + self.min_q, self.highest_r + self.min_r)
        num_cols = self.highest_r - self.lowest_r
        num_rows = self.highest_q - self.lowest_q
        initial_r = self.lowest_r
        q = self.highest_q
        r = self.highest_r
        while q > self.lowest_q:
            q -= 2
            r += 1
        max_r = r + 1
        q = self.lowest_q
        r = self.lowest_r
        while q < self.highest_q:
            q += 2
            r -= 1
        min_r = r

        print('box',
            (self.lowest_q+ self.min_q, self.lowest_r+ self.min_r),
            (self.highest_q+ self.min_q, min_r+ self.min_r),
            (self.lowest_q+ self.min_q, max_r+ self.min_r),
            (self.highest_q+ self.min_q, self.highest_r+ self.min_r))

        starting_r = self.lowest_r
        ending_r = min_r
        while tiles_found < num_tiles_to_print:
            q = self.lowest_q - (alternate % 2)
            r = starting_r
            print('line', (q + self.min_q, r + self.min_r), ' to ', (self.highest_q+ self.min_q, ending_r + self.min_r))
            print('starting line', q + self.min_q, r + self.min_r)
            line = []
            while r >= ending_r:
                tile = self._grid[q][r]
                line.append(tile)
                print(q + self.min_q, r + self.min_r)
                if tile:
                    tiles_found +=1
                q += 2
                r -= 1
            lines.append(line)
            if starting_r > max_r:
                print('!!! ------- error ------- !!!')
                break
            alternate = (alternate + 1)
            starting_r += alternate % 2
            ending_r += alternate % 2

        # print(lines)
        alternate = 0
        output = ''
        # lines = list(filter(lambda line: len(list(filter(bool,line))) > 0,lines))
        for row, line in enumerate(lines):
            for i in range(5):
                if (alternate % 2) == 0:
                    output += '         '
                for col, tile in enumerate(line):
                    if tile:
                        if i == 0:
                            output += str(tile.orientation)
                            output += ' _____  '
                        elif i == 1:
                            output += ' /     \\ '
                        elif i == 2:
                            output += '/' + '{:^7}'.format(tile.name[0:7]) + '\\'
                        elif i == 3:
                            output += '\\' + '{:^7}'.format(str(tile.q)+','+str(tile.r)) + '/'
                        elif i == 4:
                            output += ' \_____/ '
                        output += ' ' * 9
                    else:
                        output += ' ' * 18
                output += '\n'
            alternate += 1
        print(output)


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
        return self.grid.set_neighbor(tile.q, tile.r, direction, new_tile)

    def get_starting_direction(self, from_tile, to_tile):
        for i in range(6):
            if self.get_neighbor(to_tile, i) == from_tile:
                return i

    def print(self):
        self.grid.print()
