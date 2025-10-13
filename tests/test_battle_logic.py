from battle_logic import BattleLogic
from type_rules import StandardTypeRule

# We instantiate the battle logic object once for testing
# Using the default ruleset
battle_system = BattleLogic(rule_set=StandardTypeRule())
# WE KEEP THE ADVANTAGENS_DE_TIPOS VARIABLE ONLY IF IT IS USED IN OTHER TESTS.
VANTAGENS_DE_TIPOS = StandardTypeRule().get_advantages()


# Test for the method that checks the strength of one type against another
def test_is_strong_against():
    # Now we call the battle_system instance method
    # Clear Advantage Test: Fire is strong against Grass
    assert battle_system.is_strong_against("fire", "grass") == True

    # Disadvantage/Neutral Test: Fire is NOT strong against Water
    assert battle_system.is_strong_against("fire", "water") == False

    # Non-Existent Type Test
    assert battle_system.is_strong_against("fake", "normal") == False

    # Complex Advantage Test: Ground is strong against Stone
    assert battle_system.is_strong_against("ground", "rock") == True


def test_determine_winner_p1_wins():
    # Charizard (Fire/Flying) vs Bulbasaur (Grass/Poison)
    # Fire > Grass (+1 p1); Flying > Grass (+1 p1)
    results = battle_system.determine_winner(
        "charizard", ["fire", "flying"], "bulbasaur", ["grass", "poison"])
    assert "Charizard's Fire type is strong against Bulbasaur's Grass type" in results[0]
    # Must declare Charizard as the winner
    assert "Winner: Charizard." in results[-1]


def test_determine_winner_p2_wins():
    # Blastoise (Water) vs Charizard (Fire/Flying)
    # Water > Fire (+1 p2)
    results = battle_system.determine_winner(
        "charizard", ["fire", "flying"], "blastoise", ["water"])
    # We adjusted the assert line because the logic now always shows the attacker/defender:
    # P2 (Blastoise) has a strong type (Water) against P1's type (Fire)
    assert "Blastoise's Water type is strong against Charizard's Fire type" in results[0]
    # Must declare Blastoise as the winner
    assert "Winner: Blastoise." in results[-1]


def test_determine_winner_tie_by_no_advantage():
    p1_types = ["normal"]
    p2_types = ["poison"]
    results = battle_system.determine_winner(
        "snorlax", p1_types, "arbok", p2_types)
    assert "No type advantage found. It's a technical draw!" in results[0]
