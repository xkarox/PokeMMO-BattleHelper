from collections.abc import MutableMapping
import pokepy 
import json



class Database_service():

    def __init__(self):
        self.client = pokepy.V2Client()
    
    def get_pokemon( self, pokemon_name: str ):

        try:
            pokemon = self.client.get_pokemon( pokemon_name.lower() )
        except:
            print('[ERROR] Could not get pokemon from api')
            
        return pokemon
        
        
    def get_pokemon_types( self, pokemon ):
        pokemon_types = []
        
        try:
            for types in pokemon[0].types:
                print(types.type.name)
                pokemon_types.append(types.type.name)
        except:
            print('[ERROR] Could not get pokemon types')
    
        return pokemon_types

        