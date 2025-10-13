from battle_logic import BattleLogic
from type_rules import StandardTypeRule

# Instanciamos o objeto de lógica de batalha uma vez para os testes
# Usando o conjunto de regras padrão
battle_system = BattleLogic(rule_set=StandardTypeRule())
# MANTEMOS A VARIAVEL VANTAGENS_DE_TIPOS APENAS SE FOR USADA EM OUTROS TESTES.
VANTAGENS_DE_TIPOS = StandardTypeRule().get_advantages()


# Teste para o método que verifica a força de um tipo contra outro
def test_is_strong_against():
    # Agora chamamos o método da instância battle_system
    # Teste de Vantagem Clara: Fogo é forte contra Grama
    assert battle_system.is_strong_against("fire", "grass") == True

    # Teste de Desvantagem/Neutro: Fogo NÃO é forte contra Água
    assert battle_system.is_strong_against("fire", "water") == False

    # Teste de Tipo Inexistente
    assert battle_system.is_strong_against("fake", "normal") == False

    # Teste de Vantagem complexa: Chão é forte contra Pedra
    assert battle_system.is_strong_against("ground", "rock") == True

# Teste para a lógica completa de determinação de vencedor


def test_determine_winner_p1_wins():
    # Charizard (Fire/Flying) vs Bulbasaur (Grass/Poison)
    # Fire > Grass (+1 p1); Flying > Grass (+1 p1)
    results = battle_system.determine_winner(
        "charizard", ["fire", "flying"], "bulbasaur", ["grass", "poison"])
    assert "Charizard's Fire type is strong against Bulbasaur's Grass type" in results[0]
    # Deve declarar o Charizard como vencedor
    assert "Winner: Charizard." in results[-1]


def test_determine_winner_p2_wins():
    # Blastoise (Water) vs Charizard (Fire/Flying)
    # Water > Fire (+1 p2)
    results = battle_system.determine_winner(
        "charizard", ["fire", "flying"], "blastoise", ["water"])
    # Ajustamos a linha de assert porque a lógica agora sempre mostra o atacante/defensor:
    # O P2 (Blastoise) tem um tipo forte (Water) contra o tipo do P1 (Fire)
    assert "Blastoise's Water type is strong against Charizard's Fire type" in results[0]
    # Deve declarar o Blastoise como vencedor
    assert "Winner: Blastoise." in results[-1]


def test_determine_winner_tie_by_no_advantage():
    # Empate: Nenhum tipo tem vantagem sobre o outro (ex: Normal vs Poison)
    p1_types = ["normal"]
    p2_types = ["poison"]
    results = battle_system.determine_winner(
        "snorlax", p1_types, "arbok", p2_types)
    assert "No type advantage found. It's a technical draw!" in results[0]

# O resto dos testes deve ser revisado, mas esta é a estrutura principal.
