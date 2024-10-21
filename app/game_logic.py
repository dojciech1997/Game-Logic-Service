import uuid

class GameManager:
    def __init__(self):
        self.games = {}

    def start_new_game(self, player1: str, player2: str) -> str:
        game_id = str(uuid.uuid4())
        self.games[game_id] = {
            "players": [player1, player2],
            "moves": [],
            "status": "ongoing"
        }
        return game_id

    def make_move(self, game_id: str, player: str, move: str) -> str:
        if game_id not in self.games:
            return "Invalid game ID"

        game = self.games[game_id]

        if game["status"] != "ongoing":
            return "Game is already finished"

        game["moves"].append({"player": player, "move": move})

        if len(game["moves"]) > 10:
            game["status"] = "finished"

        return "Move registered"

    def get_game_status(self, game_id: str):
        if game_id not in self.games:
            return "Invalid game ID"

        return self.games[game_id]