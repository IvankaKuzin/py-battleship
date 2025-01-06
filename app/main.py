class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.rows = row
        self.columns = column
        self.is_alive = is_alive
        self.game_deck = [["~" for _ in range(column)] for _ in range(row)]

    def __getitem__(self, index: tuple) -> list:
        row, col = index
        if 0 <= row < self.rows and 0 <= col < self.columns:
            return self.game_deck[row][col]

    def __setitem__(self, index: tuple, value: str) -> None:
        row, col = index
        if 0 <= row < self.rows and 0 <= col < self.columns:
            self.game_deck[row][col] = value

    def __str__(self) -> str:
        return "\n".join(" ".join(row) for row in self.game_deck)


class Ship:
    def __init__(
            self,
            start: tuple,
            end: tuple,
            is_drowned: bool = False
    ) -> None:
        self.start = start
        self.end = end
        self.is_drowned = is_drowned
        self.hits = 0

    def put_ship(self, deck: Deck) -> Deck:
        if self.start[0] == self.end[0]:
            for x_coord in range(self.start[1], self.end[1] + 1):
                deck[self.start[0], x_coord] = "□"
        else:
            for y_coord in range(self.start[0], self.end[0] + 1):
                deck[y_coord, self.start[1]] = "□"

        return deck

    def get_deck(self, row: int, column: int) -> bool:
        if (
            self.start[0] <= row <= self.end[0]
            and self.start[1] <= column <= self.end[1]
        ):
            return True
        return False

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if not deck:
            return "Miss!"

        self.hits += 1

        ship_length = max(
            abs(self.start[0] - self.end[0]) + 1,
            abs(self.start[1] - self.end[1]) + 1
        )

        if self.hits == ship_length:
            self.is_drowned = True
            return "Sunk!"

        return "Hit!"


class Battleship:
    def __init__(self, ships: list) -> None:
        self.game_deck = Deck(10, 10)
        self.ships = [
            Ship(ships[i][0], ships[i][1])
            for i in range(len(ships))
        ]
        self.field = {}
        self.hits = set()

    def start_game(self) -> Deck:
        for ship in self.ships:
            if ship.start[0] == ship.end[0]:
                for x_coord in range(ship.start[1], ship.end[1] + 1):
                    self.game_deck[ship.start[0], x_coord] = "□"
            else:
                for y_coord in range(ship.start[0], ship.end[0] + 1):
                    self.game_deck[y_coord, ship.start[1]] = "□"

        return self.game_deck

    def fire(self, location: tuple) -> str:
        print(location)
        row, col = location

        if location in self.hits:
            return "Already hit!"

        self.hits.add(location)

        for ship in self.ships:
            if ship.get_deck(row, col):
                result = ship.fire(row, col)

                if result == "Sunk!":
                    if ship.start[0] == ship.end[0]:
                        for x_coord in range(ship.start[1], ship.end[1] + 1):
                            self.game_deck[ship.start[0], x_coord] = "x"
                    else:
                        for y_coord in range(ship.start[0], ship.end[0] + 1):
                            self.game_deck[y_coord, ship.start[1]] = "x"
                elif result == "Hit!":
                    self.game_deck[row, col] = "*"

                return result

        self.game_deck[row, col] = "•"
        return "Miss!"
