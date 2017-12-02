import random

class Boat(object):
    current_beach = None

    def __init__(self, player):
        self.player = player

    def return_to_player(self):
        assert self.current_beach is None
        if self in self.player.placed_boats:
            self.player.placed_boats.remove(self)
            self.player.available_boats.append(self)


class Player(object):
    def __init__(self, name, num_boats=15):
        self.name = name
        self.available_boats = [Boat(self) for _ in range(num_boats)]
        self.placed_boats = set()

    def get_island_expansion_choices(self):
        return list(set(map(lambda boat: boat.current_beach.tile, self.placed_boats)))

    def get_boat(self):
        return self.available_boats.pop(0)

    def place_boat(self, beach, boat):
        beach.place_boat(boat)
        self.placed_boats.add(boat)

    def expand(self, island_tile):
        """
        Expand boats on the specified island tile.
        """
        # sanity check that we're allowed to expand
        num_boats = island_tile.count_player_boats(self)
        assert num_boats > 0
        num_boats = min(num_boats, len(island_tile.beaches), len(self.available_boats))
        boats = []
        for i in range(num_boats):
            boats.append(self.get_boat())
        self.place_boats(island_tile, boats)

    def place_initial_boat(self, starting_tile):
        """
        Decide where to place a boat following the rules for game setup.
        """
        raise NotImplemented()


class RandomPlayer(Player):
    def place_initial_boat(self, starting_tile):
        """
        Randomly place a boat in a legal starting position.
        """
        open_beaches = list(filter(lambda beach: beach.num_open_moorings > 1, starting_tile.beaches))
        random_beach = random.choice(open_beaches)
        self.place_boat(random_beach, self.get_boat())

    def choose_island_to_expand(self):
        """
        Randomly choose a valid island to expand on.
        """
        return random.choice(self.get_island_expansion_choices())

    def place_boats(self, island_tile, boats):
        """
        Randomly place boats on the given island tile.
        """
        random.shuffle(boats)
        for boat in boats:
            open_beaches = island_tile.open_beaches
            if open_beaches:
                random_beach = random.choice(open_beaches)
                self.place_boat(random_beach, boat)
            else:
                boat.return_to_player()

    def choose_dock(self, beach):
        """
        Randomly choose a dock to migrate from the given beach.
        """
        return random.choice(list(beach.docks))

    def choose_beach_to_migrate(self):
        beaches = set()
        for boat in self.placed_boats:
            if boat.current_beach.is_full:
                beaches.add(boat.current_beach)
        if len(beaches):
            return random.choice(list(beaches))
        return None
