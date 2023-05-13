import pokebase as pb

import json



class Database_service():

    def __init__():
        pass
    

    def get_pokemon_types(pokemon_name: str):
        pokemon = pb.pokemon(pokemon_name)
        
        pokemon_types = []
        for element in pokemon.types:
            pokemon_types.append(element.type.name)
        
        return pokemon_types
    