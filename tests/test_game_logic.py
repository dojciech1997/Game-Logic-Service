import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_start_game():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/start-game", json={"player1": "Alice", "player2": "Bob"})
        assert response.status_code == 200
        data = response.json()
        assert "game_id" in data
        assert isinstance(data["game_id"], str)

@pytest.mark.asyncio
async def test_valid_move():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        start_response = await ac.post("/start-game", json={"player1": "Alice", "player2": "Bob"})
        game_id = start_response.json()["game_id"]
        move_response = await ac.post("/play-move", json={"game_id": game_id, "player": "Alice", "move": "move1"})
        assert move_response.status_code == 200
        data = move_response.json()
        assert data["result"] == "Move registered"

@pytest.mark.asyncio
async def test_invalid_move():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        move_response = await ac.post("/play-move", json={"game_id": "invalid_game_id", "player": "Alice", "move": "move1"})
        assert move_response.status_code == 200
        data = move_response.json()
        assert data["result"] == "Invalid game ID"

@pytest.mark.asyncio
async def test_game_status():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        start_response = await ac.post("/start-game", json={"player1": "Alice", "player2": "Bob"})
        game_id = start_response.json()["game_id"]
        await ac.post("/play-move", json={"game_id": game_id, "player": "Alice", "move": "move1"})
        status_response = await ac.get(f"/game-status/{game_id}")
        assert status_response.status_code == 200
        data = status_response.json()
        print(data)
        assert data["status"]["status"] == "ongoing"
        assert len(data["status"]["moves"]) == 1

@pytest.mark.asyncio
async def test_game_end():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        start_response = await ac.post("/start-game", json={"player1": "Alice", "player2": "Bob"})
        game_id = start_response.json()["game_id"]
        for i in range(11):
            await ac.post("/play-move", json={"game_id": game_id, "player": "Alice", "move": f"move{i+1}"})
        status_response = await ac.get(f"/game-status/{game_id}")
        assert status_response.status_code == 200
        data = status_response.json()
        assert data["status"]["status"] == "finished"
