import pokebase as pb

import json



class Database_service():

    def __init__(self):
        pass
    
    def get_pokemon( self, pokemon_name: str ):
        pokemon = pb.pokemon(pokemon_name.lower())
        
        return pokemon
        
        
    def get_pokemon_types( self, pokemon: pb.interface.APIResource ):
        test = pokemon
        pokemon_types = []
        
        try:
            for element in pokemon.types:
                type = element.type.name.lower()
                pokemon_types.append(element.type.name)
        except:
            pass
        return pokemon_types
    