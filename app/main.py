from fastapi import FastAPI
from app.game_logic import GameManager

app = FastAPI()

game_manager = GameManager()

@app.post("/start-game")
async def start_game(player1: str, player2: str):
    game_id = game_manager.start_new_game(player1, player2)
    return {"game_id": game_id}

@app.post("/play-move")
async def play_move(game_id: str, player: str, move: str):
    result = game_manager.make_move(game_id, player, move)
    return {"result": result}

@app.get("/game-status/{game_id}")
async def game_status(game_id: str):
    status = game_manager.get_game_status(game_id)
    return {"status": status}
