from flask import Flask, request, jsonify
import requests
from battle_logic import determine_winner
from pokemon_data_factory import PokemonFactory
# Base URL for the PokeAPI
POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon/"

# Flask instance creation
# __name__ argument helps Flask to know where to find resources like templates.
app = Flask(__name__)

# The /battle endpoint should accept only POST requests


@app.route('/battle', methods=['POST'])
def battle():
    """Receives the Pokemon ids, calls PokeAPI and starts the battle."""

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

    # 4. Battle logic
    results_list = determine_winner(
        p1_name=pokemon1_data['name'],  # type: ignore
        p1_types=pokemon1_data['types'],  # type: ignore
        p2_name=pokemon2_data['name'],  # type: ignore
        p2_types=pokemon2_data['types']  # type: ignore
    )

    return jsonify({
        "pokemon1": pokemon1_data['name'],  # type: ignore
        "pokemon2": pokemon2_data['name'],  # type: ignore
        "results": results_list
    }), 200


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

# Funções que usam a nova lógica de Factory


def get_pokemon_data(pokemon_id):
    """
    Orchestrates the search and creation of the simplified data object.
    """
    # 1. Fetches the raw data (responsibility of the fetch function)
    raw_data = fetch_pokemon_json(pokemon_id)

    # 2. Creates the simplified data object (Factory's responsibility)
    return PokemonFactory.create_data(raw_data)

# A simple route to test if the server is running


@app.route('/')
def home():
    return "Hello, World!"


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
