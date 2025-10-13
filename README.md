# Pokémon Battle API

## Objective

This is a REST API developed in Python with Flask to simulate a Pokémon battle. The system allows you to select two Pokémon, obtain their types through the PokeAPI, and determine the winner based on a table of type advantages.

## Installation and Execution

1. **Clone the repository:**

```bash
git clone git@github.com:viniciusvalentee/pokemon-battle-api.git
```

2. **Create and activate the virtual environment:**

```bash
python3 -m venv venv

Linux/MacOS: source venv/bin/activate
Windows: .\venv\Scripts\activate
```

3. **Install the dependencies:**

```bash
pip install -r requirements.txt
```

4. **Run the server:**

```bash
python app.py
```

The server will be running at `http://127.0.0.1:5000/`.

## 🚀 Using the `/battle` Endpoint

The `/battle` endpoint accepts **POST** requests with a JSON body containing the IDs of two Pokémon.

### ➡️ Request

You can test using `curl` (terminal) or tools like Postman.

**Example (Pikachu vs. Squirtle):**

```bash
curl -X POST [http://127.0.0.1:5000/battle](http://127.0.0.1:5000/battle) \
-H "Content-Type: application/json" \
-d '{"pokemon1": 25, "pokemon2": 7}'
```

- `pokemon1`: 25 (Pikachu - Electric)
- `pokemon2`: 7 (Squirtle - Water)

  ### Since the Electric type is strong against Water, Pikachu is the winner.

  ```json
  {
    "pokemon1": "pikachu",
    "pokemon2": "squirtle",
    "results": [
      "Pikachu's Electric type is strong against Squirtle's Water type.",
      "Winner: Pikachu for having more advantages (1 to 0)."
    ]
  }
  ```

  ### If Pokémon with neutral types (such as Normal) are compared:

  ```json
  {
    "pokemon1": "snorlax",
    "pokemon2": "rattata",
    "results": ["No type advantage found. It's a technical draw!"]
  }
  ```

  ### If a Pokémon ID does not exist (e.g. 9999):

  ```
  {
    "error": "Pokémon with ID 9999 not found."
  }
  ```

  ### Running Automated Tests

  To ensure that your battle logic and API calls are correct, run pytest in the project root:

  ```bash
  python -m pytest
  ```
