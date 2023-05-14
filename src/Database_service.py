import pokebase as pb

import json



class Database_service():

    def __init__(self):
        pass
    
    def get_pokemon( self, pokemon_name: str ):
        pokemon = pb.pokemon(pokemon_name)
        
        return pokemon
        
        
    def get_pokemon_types( self, pokemon: pb.interface.APIResource ):
        
        pokemon_types = []
        for element in pokemon.types:
            pokemon_types.append(element.type.name)
        
        return pokemon_types
    