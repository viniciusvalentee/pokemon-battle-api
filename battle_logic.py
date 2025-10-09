# Dictionary that stores the advantages table
# Format: {ATTACKER_TYPE: [TYPES_WHICH_IT_IS_STRONG_AGAINST]}
ADVANTAGES_OF_TYPES = {
    "fire": ["grass", "bug", "ice"],
    "water": ["fire", "ground", "rock"],
    "grass": ["water", "ground", "rock"],
    "electric": ["water", "flying"],
    "ground": ["fire", "electric", "rock"],
    "flying": ["grass", "fighting", "bug"],
    "fighting": ["normal", "rock", "ice"],
    "fairy": ["fighting", "dragon", "dark"],
    "dark": ["psychic", "ghost"],
    "psychic": ["fighting", "poison"],
}


def is_strong_against(attacking_type, defending_type):
    """
    Checks if one type has an advantage over the other.
    """
    # If the attacker type is in our dictionary AND the defender type is in the advantages list
    if attacking_type in ADVANTAGES_OF_TYPES:
        if defending_type in ADVANTAGES_OF_TYPES[attacking_type]:
            return True
    return False


def determine_winner(p1_name, p1_types, p2_name, p2_types):
    """
    Compares the types of the two Pokémon and determines the winner.

    Returns: A list of strings describing the results of the type battle.
    """
    results = []
    p1_score = 0
    p2_score = 0

    # 1. Comparison: Pokémon 1 attacks Pokémon 2
    for p1_type in p1_types:
        for p2_type in p2_types:
            if is_strong_against(p1_type, p2_type):
                results.append(
                    f"{p1_name.capitalize()}'s {p1_type.capitalize()} type is strong against {p2_name.capitalize()}'s {p2_type.capitalize()} type.")
                p1_score += 1
            elif is_strong_against(p2_type, p1_type):
                # If P2's type is strong against P1's type, that is a weakness of P1
                results.append(
                    f"{p2_name.capitalize()}'s {p2_type.capitalize()} type is strong against {p1_name.capitalize()}'s {p1_type.capitalize()} type.")
                p2_score += 1

    # If the results list is empty, it means there were no direct benefits.
    if not results:
        # Requirement 4: If one type has no advantage over the other, a draw must be declared.
        results.append(
            "No type advantage found. It's a technical draw!")

    # If there are advantages, we will determine the winner by the total score.
    if p1_score > p2_score:
        results.append(
            f"Winner: {p1_name.capitalize()} for having more advantages ({p1_score} a {p2_score}).")
    elif p2_score > p1_score:
        results.append(
            f"Winner: {p2_name.capitalize()} for having more advantages ({p2_score} a {p1_score}).")
    elif p1_score > 0 and p1_score == p2_score:
        results.append(
            f"It's a tie! Both Pokémon have the same number of advantages ({p1_score} a {p2_score}).")

    # If p1_score and p2_score are both 0, the tie has already been declared in `if not results`.

    return results
