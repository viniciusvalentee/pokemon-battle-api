from type_rules import TypeAdvantageRule, StandardTypeRule


class BattleLogic:
    """
    Core class for battle logic, injecting the rules.
    (OCP: Closed, as it doesn't need to be changed if new rules appear)
    """

    def __init__(self, rule_set: TypeAdvantageRule = StandardTypeRule()):
        """
        Optionally accepts a Rule Set.
        By default, it uses the StandardTypeRule.
        """
        self.rules = rule_set.get_advantages()

    def is_strong_against(self, attacking_type, defending_type):
        """
        Checks strength using the injected ruleset.
        """
        if attacking_type in self.rules:
            if defending_type in self.rules[attacking_type]:
                return True
        return False

    def determine_winner(self, p1_name, p1_types, p2_name, p2_types):
        """
        Compares the types of both Pokémon and determines the winner.
        The scoring logic remains the same, but now uses self.is_strong_against.
        """
        results = []
        p1_score = 0
        p2_score = 0

        # 1. Comparison: Pokémon 1 attacks Pokémon 2
        for p1_type in p1_types:
            for p2_type in p2_types:
                if self.is_strong_against(p1_type, p2_type):
                    results.append(
                        f"{p1_name.capitalize()}'s {p1_type.capitalize()} type is strong against {p2_name.capitalize()}'s {p2_type.capitalize()} type.")
                    p1_score += 1
                elif self.is_strong_against(p2_type, p1_type):
                    results.append(
                        f"{p2_name.capitalize()}'s {p2_type.capitalize()} type is strong against {p1_name.capitalize()}'s {p1_type.capitalize()} type.")
                    p2_score += 1

        # If the results list is empty, it means there were no direct benefits.
        if not results and p1_score == 0 and p2_score == 0:
            results.append(
                "No type advantage found. It's a technical draw!")

        if p1_score > p2_score:
            results.append(
                f"Winner: {p1_name.capitalize()}.")
        elif p2_score > p1_score:
            results.append(
                f"Winner: {p2_name.capitalize()}.")
        elif p1_score > 0 and p1_score == p2_score:
            results.append(
                f"It's a tie! Both Pokémon have the same number of advantages.")

        return results
