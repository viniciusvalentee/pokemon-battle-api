from flask import Flask, request, jsonify
import requests

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
        pokemon1_details = get_pokemon_details(pokemon1_id)
        pokemon2_details = get_pokemon_details(pokemon2_id)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Error fetching data from PokeAPI.",
                        "details": str(e)}), 503
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404

    # TODO: 4. Battle logic
    # Here, we would use the details to extract types and calculate the result.
    # For now, we will just return the fetched details.
    return jsonify({
        "pokemon1": pokemon1_details,
        "pokemon2": pokemon2_details,
        "message": "Battle logic not implemented yet."
    }), 200


def get_pokemon_details(pokemon_id):
    """"Make the API call to PokeAPI and return JSON data."""
    url = f"{POKEAPI_URL}{pokemon_id}/"  # Creates the URL: https://pokeapi.co/api/v2/pokemon/{id}

    # Make the GET request to PokeAPI
    response = requests.get(url)

    # Check if the response was successful
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        raise ValueError(f"Pokemon with id {pokemon_id} not found.")
    else:
        response.raise_for_status()  # Raise an error for other bad responses

# A simple route to test if the server is running


@app.route('/')
def home():
    return "Hello, World!"


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
