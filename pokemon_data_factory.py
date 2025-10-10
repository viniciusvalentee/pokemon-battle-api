# pokemon_data_factory.py

class PokemonFactory:
    """
    Implements the Factory Method Pattern.
    Its sole responsibility is to construct and return a simplified dictionary
    of Pokémon data (applies the SRP).
    """

    @staticmethod
    def extract_types(pokemon_data: dict) -> list:
        """
        Extracts the list of type names from the API's raw JSON.
        This logic was previously in app.py, but is now part of Factory.
        """
        types_list = []
        for type_info in pokemon_data.get('types', []):
            type_name = type_info['type']['name']
            types_list.append(type_name)
        return types_list

    @classmethod
    def create_data(cls, pokemon_data: dict) -> dict:
        """
        Factory method that creates and returns the simplified data object.
        """
        # Extracts the required data using the helper method
        types = cls.extract_types(pokemon_data)
        name = pokemon_data.get('name')

        # Returns a simplified dictionary
        return {
            'name': name,
            'types': types
        }

# Example usage:
# data = requests.get(...).json()
# clean_pokemon = PokemonFactory.create_data(data)
