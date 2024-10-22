from fastapi import FastAPI, WebSocket
from app.game_logic import GameManager
from pydantic import BaseModel
import json

app = FastAPI()

game_manager = GameManager()


class StartGameRequest(BaseModel):
    player1: str
    player2: str


class PlayMoveRequest(BaseModel):
    game_id: str
    player: str
    move: str


@app.post("/start-game")
async def start_game(request: StartGameRequest):
    game_id = game_manager.start_new_game(request.player1, request.player2)
    return {"game_id": game_id}


@app.post("/play-move")
async def play_move(request: PlayMoveRequest):
    result = game_manager.make_move(request.game_id, request.player, request.move)
    return {"result": result}


@app.get("/game-status/{game_id}")
async def game_status(game_id: str):
    status = game_manager.get_game_status(game_id)
    return {"status": status}


@app.websocket("/ws/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        move = json.loads(data)
        result = game_manager.make_move(game_id, move["player"], move["move"])
        await websocket.send_text(result)
