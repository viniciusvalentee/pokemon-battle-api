import pytest
import requests_mock
import json
from app import app, POKEAPI_URL

# Setting up the Flask fixture (preparation) for testing


@pytest.fixture
def client():
    # Set Flask to test mode
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client  # The 'yield' is where the testing happens


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
