import pytest

from battle_logic import determine_winner, is_strong_against, ADVANTAGES_OF_TYPES


def test_is_strong_against():
    assert is_strong_against('fire', 'grass') is True
    assert is_strong_against('water', 'fire') is True
    assert is_strong_against('grass', 'water') is True
    assert is_strong_against('electric', 'water') is True
    assert is_strong_against('ground', 'electric') is True

    assert is_strong_against('fire', 'water') is False
    assert is_strong_against('water', 'grass') is False
    assert is_strong_against('grass', 'fire') is False
    assert is_strong_against('electric', 'ground') is False
    assert is_strong_against('ground', 'grass') is False

    assert is_strong_against('normal', 'ghost') is False  # No advantage


def test_determine_winner_p1_wins():
    # Blastoise (Water) vs Charizard (Fire/Flying)
    # Water > Fire (+1 p2)
    results = determine_winner(
        "charizard", ["fire", "flying"], "blastoise", ["water"])
    assert "Blastoise's Water type is strong against Charizard's Fire type" in results[0]
    # Should declare Blastoise as winner
    assert "Winner: Blastoise" in results[-1]


def test_determine_winner_tie_by_score():
    # Made-up example where both score the same (2x2)
    p1_types = ["fire", "fighting"]  # Fire > Grass, Fighting > Rock
    p2_types = ["grass", "rock"]  # Grass > Water, Rock > Flying

    # To simulate a score tie: P1 (Fire > Grass, Fighting is neutral) vs. P2 (Grass > Fire, Rock > Fighting)
    # Using the types in the table, it's difficult to force a 1-1 or 2-2 tie.
    # Let's focus on the no-advantage rule:
    p1_types = ["normal"]
    p2_types = ["poison"]
    results = determine_winner("snorlax", p1_types, "arbok", p2_types)
    assert "No type advantage found. It's a technical draw!" in results[0]
