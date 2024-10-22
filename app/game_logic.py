import uuid
import redis
import random
import json

r = redis.Redis(host="redis", port=6379, db=0)


class GameManager:
    def __init__(self):
        self.redis_client = r

    def _generate_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = [f'{rank} of {suit}' for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def start_new_game(self, player1: str, player2: str) -> str:
        game_id = str(uuid.uuid4())
        deck = self._generate_deck()
        game_state = {
            "players": [player1, player2],
            "deck": deck,
            "moves": [],
            "status": "ongoing"
        }
        self.redis_client.set(game_id, json.dumps(game_state))
        return game_id

    def make_move(self, game_id: str, player: str, move: str) -> str:
        game_state_json = self.redis_client.get(game_id)
        if not game_state_json:
            return "Invalid game ID"
        game_state = json.loads(game_state_json)
        if game_state["status"] != "ongoing":
            return "Game is already finished"
        game_state["moves"].append({"player": player, "move": move})
        if len(game_state["moves"]) > 10:
            game_state["status"] = "finished"
        self.redis_client.set(game_id, json.dumps(game_state))
        return "Move registered"

    def get_game_status(self, game_id: str):
        game_state_json = self.redis_client.get(game_id)
        if not game_state_json:
            return "Invalid game ID"
        game_state = json.loads(game_state_json)
        return game_state