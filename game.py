import random
from board import Board


class GameOver(Exception):
    pass


class Game(object):
    def __init__(self, starting_tile, tile_stack, num_initial_boats=2):

        random.shuffle(tile_stack)
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
        return tile

    @property
    def is_over(self):
        remaining_islands = list(filter(lambda tile: tile.is_island == True, self.tile_stack))
        remaining_waters = list(filter(lambda tile: tile.is_water == True, self.tile_stack))
        return len(remaining_islands) == 0 or len(remaining_waters) == 0

    def setup(self):
        for i in range(self.num_initial_boats):
            for player in self.players:
                player.place_initial_boat(self.starting_tile)

    def resolve_migrations(self, player):
        # until all this player's migrations are complete...
        while True:
            beach = player.choose_beach_to_migrate()
            if not beach:
                # Player could not migrate..
                return
            direction = player.choose_dock(beach)
            current_tile = beach.tile
            print('!!! migrating tile in direction:', direction)
            print(current_tile)
            current_boats = beach.remove_all()
            # until current migration is complete...
            while True:
                next_tile = self.board.get_neighbor(current_tile, direction)
                # existing tile
                if next_tile:
                    # determine starting side of the existing tile
                    direction = self.board.get_starting_direction(current_tile, next_tile)
                else:
                    next_tile = self.get_tile()

                    print('placing tile')
                    self.board.set_neighbor(current_tile, direction, next_tile)

                    # starting direction (side) is always 0 for new tiles
                    direction = 0

                current_tile = next_tile

                if current_tile.is_water:
                    # try to pass the water tile
                    print('still sailing...')
                    print(current_tile)
                    if not self.is_over and current_tile.can_pass(current_boats, direction):
                        old_direction = direction
                        direction = current_tile.get_end(direction)
                        continue
                    else:
                        print('!!! lost at sea...')
                        # lost at sea... return boats to player and stop picking tiles
                        for boat in current_boats:
                            boat.return_to_player()

                        # End immediately if the last tile is a water
                        if self.is_over:
                            raise GameOver()
                        break
                elif current_tile.is_island:
                    # landfall! place boats and stop picking tiles.
                    player.place_boats(current_tile, current_boats)
                    print('made landfall')
                    print(current_tile)
                    if self.is_over:
                        raise GameOver()
                    break

    def play_turn(self, player):
        print(player)
        island_to_expand = player.choose_island_to_expand()
        if not island_to_expand:
            # player couldn't expand anywhere, so let's just place 2 boats on tonga
            player.place_boats(self.starting_tile, [player.get_boat(), player.get_boat()])
        else:
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
            for player in self.players:
                print(player)
        except KeyboardInterrupt:
            print('Interrupted')

        self.board.print()
        self.board.serialize()
