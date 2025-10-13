# 🐉 Pokémon Battle API

## 🧭 Objective

This is a REST API developed in **Python + Flask** to simulate a Pokémon battle.  
It allows selecting two Pokémon, fetching their types from the **PokeAPI**, and determining the winner based on a table of type advantages.

---

## ⚙️ Installation and Execution

### 1. Clone the repository
```bash
git clone git@github.com:viniciusvalentee/pokemon-battle-api.git
```

### 2. Create and activate the virtual environment
```bash
python -m venv venv
```

**Linux/MacOS:**
```bash
source venv/bin/activate
```

**Windows (PowerShell):**
```bash
venv\Scripts\activate
```

### 3. Install the dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the server
```bash
python app.py
```

The server will be available at:  
👉 `http://127.0.0.1:5000/`

---

## 🎮 Game Flow and Scoreboard

The application keeps a **temporary in-memory scoreboard** while the server is running.  
You must start the game before any battles can occur.

---

## 1️⃣ Start the Game — `POST /start`

Registers two players and initializes the scoreboard (0–0).

### ➡️ Request Body
```json
{
  "player1_name": "Ash",
  "player2_name": "Gary"
}
```

---

### 🧩 Examples

#### 🐧 Linux / MacOS
```bash
curl -X POST http://127.0.0.1:5000/start      -H "Content-Type: application/json"      -d '{"player1_name": "Ash", "player2_name": "Gary"}'
```

#### 🪟 Windows (CMD)
```cmd
curl -X POST http://127.0.0.1:5000/start -H "Content-Type: application/json" -d "{\"player1_name\": \"Ash\", \"player2_name\": \"Gary\"}"
```

#### 📬 Postman
- **Method:** POST  
- **URL:** `http://127.0.0.1:5000/start`  
- **Body → raw → JSON:**  
  ```json
  {
    "player1_name": "Ash",
    "player2_name": "Gary"
  }
  ```

---

### ⬅️ Success Response
```json
{
  "players": "Ash vs Gary",
  "scoreboard": {
    "player1_name": "Ash",
    "player1_score": 0,
    "player2_name": "Gary",
    "player2_score": 0
  },
  "status": "Game started successfully!"
}
```

---

## 2️⃣ Battle — `POST /battle`

Calculates the winner and updates the scoreboard.

### ➡️ Request Body
```json
{
  "pokemon1": 7,
  "pokemon2": 4
}
```

(Example: Ash’s **Squirtle [Water]** vs Gary’s **Charmander [Fire]**)

---

### 🧩 Examples

#### 🐧 Linux / MacOS
```bash
curl -X POST http://127.0.0.1:5000/battle      -H "Content-Type: application/json"      -d '{"pokemon1": 7, "pokemon2": 4}'
```

#### 🪟 Windows (CMD)
```cmd
curl -X POST http://127.0.0.1:5000/battle -H "Content-Type: application/json" -d "{\"pokemon1\": 7, \"pokemon2\": 4}"
```

#### 📬 Postman
- **Method:** POST  
- **URL:** `http://127.0.0.1:5000/battle`  
- **Body → raw → JSON:**  
  ```json
  {
    "pokemon1": 7,
    "pokemon2": 4
  }
  ```

---

### ⬅️ Response Example
```json
{
  "pokemon1": "squirtle",
  "pokemon2": "charmander",
  "results": [
    "Squirtle's Water type is strong against Charmander's Fire type.",
    "Winner: Squirtle."
  ],
  "round_winner": "Ash",
  "scoreboard": {
    "player1_name": "Ash",
    "player1_score": 1,
    "player2_name": "Gary",
    "player2_score": 0
  }
}
```

---

### ⚠️ Edge Cases

#### 🆚 Neutral Types (no advantage)
```json
{
  "pokemon1": "rattata",
  "pokemon2": "snorlax",
  "results": [
    "No type advantage found. It's a technical draw!"
  ],
  "round_winner": "Nobody (tie)"
}
```

#### ❌ Invalid Pokémon ID
```json
{
  "error": "Pokémon with ID 9999 not found."
}
```

---

## 3️⃣ View Scoreboard — `GET /scoreboard`

Returns the current scores and players.

---

### 🧩 Examples

#### 🐧 Linux / MacOS
```bash
curl -X GET http://127.0.0.1:5000/scoreboard
```

#### 🪟 Windows (CMD)
```cmd
curl -X GET http://127.0.0.1:5000/scoreboard
```

#### 📬 Postman
- **Method:** GET  
- **URL:** `http://127.0.0.1:5000/scoreboard`

---

### ⬅️ Response
```json
{
  "player1_name": "Ash",
  "player1_score": 1,
  "player2_name": "Gary",
  "player2_score": 0
}
```

---

## 🧪 Running Automated Tests

Use **pytest** to verify the logic and API endpoints:

```bash
python -m pytest
```

---

## 🧱 Code Structure & Design Principles

- **Single Responsibility Principle (SRP)**  
  Each component has one purpose:  
  - `fetch_pokemon_json`: data fetching  
  - `PokemonFactory`: data transformation  
  - `BattleLogic`: rules & winner calculation  
  - `app.py`: routing and API endpoints  

- **Open/Closed Principle (OCP)**  
  Core logic (`BattleLogic`) is extendable via custom rule sets (e.g., `StandardTypeRule`).

- **Modular Design**  
  Files are organized and separated logically:  
  - `battle_logic.py`  
  - `pokemon_data_factory.py`  
  - `type_rules.py`

---

## 🧭 Summary of Endpoints

| Method | Endpoint | Description | Example |
|:--|:--|:--|:--|
| **POST** | `/start` | Start a new game | Register players |
| **POST** | `/battle` | Run a Pokémon battle | Compare two Pokémon IDs |
| **GET** | `/scoreboard` | View scoreboard | Current game results |
