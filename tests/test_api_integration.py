import pytest
import requests_mock
import json
from app import app, POKEAPI_URL, GLOBAL_SCOREBOARD

# Setting up the Flask fixture (preparation) for testing


@pytest.fixture
def client():
    # Set Flask to test mode
    app.config['TESTING'] = True
    GLOBAL_SCOREBOARD.clear()  # Clear the dictionary before each test
    with app.test_client() as client:
        # We reset the scoreboard at the start of each test
        yield client

    # Ensures the scoreboard is cleared again after testing
    GLOBAL_SCOREBOARD.clear()


# Mock data that the PokeAPI would return
MOCK_CHARIZARD = {
    "name": "charizard",
    "id": 6,
    "types": [
        {"slot": 1, "type": {"name": "fire", "url": "..."}},
        {"slot": 2, "type": {"name": "flying", "url": "..."}},
    ]
}
MOCK_BLASTOISE = {
    "name": "blastoise",
    "id": 9,
    "types": [
        {"slot": 1, "type": {"name": "water", "url": "..."}},
    ]
}


def test_battle_endpoint_success(client, requests_mock):
    # Simulates the PokeAPI response for IDs 6 and 9
    requests_mock.get(f"{POKEAPI_URL}6/", json=MOCK_CHARIZARD, status_code=200)
    requests_mock.get(f"{POKEAPI_URL}9/", json=MOCK_BLASTOISE, status_code=200)

    # First, we need to start the game to initialize the scoreboard
    client.post('/start', data=json.dumps({"player1_name": "Ash",
                "player2_name": "Gary"}), content_type='application/json')
    # Data we send in POST to the API
    battle_data = {"pokemon1": 6, "pokemon2": 9}

    # Makes the simulated POST request
    response = client.post('/battle',
                           data=json.dumps(battle_data),
                           content_type='application/json')

    # Check the status code and the result (Water is strong against Fire -> Blastoise wins)
    assert response.status_code == 200
    data = response.get_json()
    assert data["pokemon1"] == "charizard"
    assert data["pokemon2"] == "blastoise"
    assert "Winner: Blastoise" in data["results"][-1]


def test_battle_endpoint_invalid_id(client, requests_mock):
    client.post('/start', data=json.dumps({"player1_name": "Ash",
                "player2_name": "Gary"}), content_type='application/json')
    # Simulates PokeAPI 404 error
    requests_mock.get(f"{POKEAPI_URL}9999/", status_code=404)

    battle_data = {"pokemon1": 1, "pokemon2": 9999}

    # Simulate success for POKEMON 1 to test the error in POKEMON 2
    requests_mock.get(f"{POKEAPI_URL}1/", json=MOCK_CHARIZARD, status_code=200)

    response = client.post('/battle',
                           data=json.dumps(battle_data),
                           content_type='application/json')

    # It should return the 404 error that we handled in app.py
    assert response.status_code == 404
    assert "Pokemon with id 9999 not found." in response.get_json()[
        "error"]


def test_start_game_success(client):
    """Testa se o endpoint /start inicializa o placar corretamente."""
    player_data = {"player1_name": "Ash", "player2_name": "Gary"}
    response = client.post('/start',
                           data=json.dumps(player_data),
                           content_type='application/json')

    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "Game started successfully!"
    assert data["scoreboard"]["player1_name"] == "Ash"
    assert data["scoreboard"]["player1_score"] == 0


def test_battle_before_start_failure(client):
    """Testa se chamar /battle antes de /start retorna erro 403."""
    battle_data = {"pokemon1": 6, "pokemon2": 9}
    response = client.post('/battle',
                           data=json.dumps(battle_data),
                           content_type='application/json')

    assert response.status_code == 403
    data = response.get_json()
    assert data["error"] == "Game not started"


def test_battle_player1_wins_and_updates_score(client, requests_mock):
    """Testa se o placar atualiza corretamente quando o Jogador 1 vence."""
    # Setup: Inicia o jogo
    client.post('/start', data=json.dumps({"player1_name": "Ash",
                "player2_name": "Gary"}), content_type='application/json')

    # Mocks: P1 (Water) vs P2 (Fire). Water > Fire. P1 vence (Blastoise)
    requests_mock.get(f"{POKEAPI_URL}9/",
                      json=MOCK_BLASTOISE, status_code=200)  # P1
    requests_mock.get(f"{POKEAPI_URL}6/",
                      json=MOCK_CHARIZARD, status_code=200)  # P2

    # Batalha: P1 (9) vs P2 (6)
    battle_data = {"pokemon1": 9, "pokemon2": 6}
    response = client.post('/battle',
                           data=json.dumps(battle_data),
                           content_type='application/json')

    # Checa o placar
    assert response.status_code == 200
    data = response.get_json()
    assert data["round_winner"] == "Ash"
    assert data["scoreboard"]["player1_score"] == 1
    assert data["scoreboard"]["player2_score"] == 0


def test_battle_tie_no_score_update(client, requests_mock):
    """Testa se em caso de empate o placar não é alterado."""
    # Setup: Inicia o jogo
    client.post('/start', data=json.dumps({"player1_name": "Ash",
                "player2_name": "Gary"}), content_type='application/json')

    # Mocks: P1 (Normal) vs P2 (Normal). Empate.
    MOCK_SNORLAX = {
        "name": "snorlax",
        "id": 143,
        "types": [{"slot": 1, "type": {"name": "normal", "url": "..."}}]
    }

    requests_mock.get(f"{POKEAPI_URL}143/", json=MOCK_SNORLAX, status_code=200)
    requests_mock.get(f"{POKEAPI_URL}143/", json=MOCK_SNORLAX, status_code=200)

    # Batalha: P1 (143) vs P2 (143)
    battle_data = {"pokemon1": 143, "pokemon2": 143}
    response = client.post('/battle',
                           data=json.dumps(battle_data),
                           content_type='application/json')

    # Checa o resultado
    assert response.status_code == 200
    data = response.get_json()
    assert data["round_winner"] == "Nobody (tie)"
    assert data["scoreboard"]["player1_score"] == 0  # Deve ser zero
    assert data["scoreboard"]["player2_score"] == 0  # Deve ser zero


def test_get_scoreboard(client):
    """Testa o endpoint /scoreboard."""
    client.post('/start', data=json.dumps({"player1_name": "Ash",
                "player2_name": "Gary"}), content_type='application/json')
    response = client.get('/scoreboard')

    assert response.status_code == 200
    data = response.get_json()
    assert data["player1_name"] == "Ash"
    assert data["player1_score"] == 0
