from flask import Flask, request, jsonify
import requests
from battle_logic import BattleLogic
from pokemon_data_factory import PokemonFactory
# Base URL for the PokeAPI
POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon/"

# Flask instance creation
# __name__ argument helps Flask to know where to find resources like templates.
app = Flask(__name__)

# The /battle endpoint should accept only POST requests
# In real applications, this would be replaced by a Database or Cache (Redis).
GLOBAL_SCOREBOARD = {}
# We initialize the battle logic outside the endpoint (OCP applied)
BATTLE_SYSTEM = BattleLogic()  # Uses the default StandardTypeRule


@app.route('/start', methods=['POST'])
def start_game():
    """
    Endpoint to start the game, registering the names of both players.
    """
    global GLOBAL_SCOREBOARD
    data = request.get_json()

    if not data or 'player1_name' not in data or 'player2_name' not in data:
        return jsonify({
            "error": "Invalid request",
            "message": "The request body must contain 'player1_name' and 'player2_name'."
        }), 400

    player1 = data.get('player1_name')
    player2 = data.get('player2_name')

    GLOBAL_SCOREBOARD.clear()
    # Starts the scoreboard
    GLOBAL_SCOREBOARD.update({
        "player1_name": player1,
        "player2_name": player2,
        "player1_score": 0,
        "player2_score": 0
    })

    return jsonify({
        "status": "Game started successfully!",
        "players": f"{player1} vs {player2}",
        "scoreboard": GLOBAL_SCOREBOARD
    })


@app.route('/battle', methods=['POST'])
def battle():
    """Receives the Pokemon ids, calls PokeAPI and starts the battle."""

    global GLOBAL_SCOREBOARD

    # Validation: The game must have been started
    if not GLOBAL_SCOREBOARD:
        return jsonify({
            "error": "Game not started",
            "message": "Please call the /start endpoint first to register players."
        }), 403
    # 1. Get the JSON data from the request
    data = request.get_json()

    # 2. Basic validation of input data
    if not data or 'pokemon1' not in data or 'pokemon2' not in data:
        return jsonify({"error": "Invalid requisition.",
                        "message": "The request body should be a JSON with 'pokemon1' and 'pokemon2'"}), 400

    pokemon1_id = data['pokemon1']
    pokemon2_id = data['pokemon2']

    # Data type validation
    if not isinstance(pokemon1_id, int) or not isinstance(pokemon2_id, int) or pokemon1_id <= 0 or pokemon2_id <= 0:
        return jsonify({"error": "Invalid requisition.",
                        "message": "'pokemon1' and 'pokemon2' should be positive integers."}), 400

    # 3. Fetch Pokemon data from PokeAPI
    try:
        pokemon1_data = get_pokemon_data(pokemon1_id)
        pokemon2_data = get_pokemon_data(pokemon2_id)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Error fetching data from PokeAPI.",
                        "details": str(e)}), 503
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404

    # 1. Get pokemon names for the response
    p1_pokemon_name = pokemon1_data['name']
    p2_pokemon_name = pokemon2_data['name']

    # 4. Battle logic
    results_list = BATTLE_SYSTEM.determine_winner(
        p1_name=p1_pokemon_name,
        p1_types=pokemon1_data['types'],
        p2_name=p2_pokemon_name,
        p2_types=pokemon2_data['types']
    )

    # Logic to extract the winner and update the scoreboard
    final_result_line = results_list[-1]
    winner_name = "Nobody (tie)"  # Default value in case of tie

    # The name of the winning Pokémon is in the result line (Ex: "Winner: Squirtle...")
    if p1_pokemon_name.capitalize() in final_result_line:
        # Pokémon 1 won, so Player 1 scores.
        GLOBAL_SCOREBOARD['player1_score'] += 1
        winner_name = GLOBAL_SCOREBOARD['player1_name']
    elif p2_pokemon_name.capitalize() in final_result_line:
        # Pokémon 2 won, so Player 2 scores.
        GLOBAL_SCOREBOARD['player2_score'] += 1
        winner_name = GLOBAL_SCOREBOARD['player2_name']

    # Final return, including updated scoreboard
    return jsonify({
        "pokemon1": pokemon1_data['name'],
        "pokemon2": pokemon2_data['name'],
        "results": results_list,
        "round_winner": winner_name,
        "scoreboard": GLOBAL_SCOREBOARD
    })

# Endpoint to view the scoreboard


@app.route('/scoreboard', methods=['GET'])
def get_scoreboard():
    if not GLOBAL_SCOREBOARD:
        return jsonify({"message": "No game started."}), 200
    return jsonify(GLOBAL_SCOREBOARD)


def extract_types(pokemon_data):
    """
    Extracts the pokemon types list.
    """
    types_list = []
    # The 'types' property is a list
    for type_info in pokemon_data.get('types', []):
        # The type info is inside the 'type' dict
        # The name type is the 'name' property inside
        type_name = type_info['type']['name']
        types_list.append(type_name)

    return types_list


def fetch_pokemon_json(pokemon_id):
    """"Make the API call to PokeAPI and return JSON data."""
    url = f"{POKEAPI_URL}{pokemon_id}/"  # Creates the URL: https://pokeapi.co/api/v2/pokemon/{id}
    response = requests.get(url)

    # Check if the response was successful
    if response.status_code == 200:
        pokemon_data = response.json()
        return pokemon_data
    elif response.status_code == 404:
        raise ValueError(f"Pokemon with id {pokemon_id} not found.")
    else:
        response.raise_for_status()  # Raise an error for other bad responses


def get_pokemon_data(pokemon_id):
    """
    Orchestrates the search and creation of the simplified data object.
    """
    # 1. Fetches the raw data (responsibility of the fetch function)
    raw_data = fetch_pokemon_json(pokemon_id)

    # 2. Creates the simplified data object (Factory's responsibility)
    return PokemonFactory.create_data(raw_data)  # type: ignore

# A simple route to test if the server is running


@app.route('/')
def home():
    return "Hello, World!"


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
