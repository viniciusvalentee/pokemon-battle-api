# type_rules.py

# The interface is implicit in Python, but the documentation makes it clear
class TypeAdvantageRule:
    """
    Abstract base class for all advantage rules.
    (OCP: Closed for modification, open for extension)
    """

    # OOCP: If it is a new rule type, it must implement this method.
    def get_advantages(self) -> dict:
        """Should return a dictionary of advantages."""
        raise NotImplementedError(
            "Subclasses must implement this method.")

# Implementação Concreta 1: A Regra Padrão do Jogo


class StandardTypeRule(TypeAdvantageRule):
    """
    Implements type rules based on the test table.
    """

    VANTAGENS_DE_TIPOS = {
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

    def get_advantages(self) -> dict:
        """Returns the dictionary of advantage rules."""
        return self.VANTAGENS_DE_TIPOS

# Concrete Implementation 2: Event Rule Example (Extension)


class EventTypeRule(TypeAdvantageRule):
    """
    A new rule for a special event, without modifying the StandardTypeRule.
    (Ex: during an event, the 'normal' type becomes strong against 'ghost')
    """

    def get_advantages(self) -> dict:
        # Takes the default rules and adds the temporary rule
        rules = StandardTypeRule().get_advantages()

        # OCP: Extension. Adds the new rule without changing the Standard class.
        rules['normal'] = ['ghost']
        return rules
