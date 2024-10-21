import pytest
from app.game_logic import GameManager


@pytest.fixture
def game_manager():
    return GameManager()


def test_start_new_game(game_manager):
    game_id = game_manager.start_new_game("player1", "player2")
    assert game_id is not None
    assert game_manager.get_game_status(game_id)["status"] == "ongoing"


def test_make_move(game_manager):
    game_id = game_manager.start_new_game("player1", "player2")
    result = game_manager.make_move(game_id, "player1", "move1")
    assert result == "Move registered"
    assert len(game_manager.get_game_status(game_id)["moves"]) == 1
