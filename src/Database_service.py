from collections.abc import MutableMapping
import pokepy 
import json



class Database_service():

    def __init__(self):
        self.client = pokepy.V2Client()
    
    def get_pokemon( self, pokemon_name: str ):

        # try:
        pokemon = self.client.get_pokemon( pokemon_name.lower() )[0]
        return pokemon
        # except:
        #     print('[ERROR] Could not get pokemon from api')
            
        
        
        
    def get_pokemon_types( self, pokemon ):
        pokemon_types = []
        
        try:
            for types in pokemon.types:
                # print(types.type.name)
                pokemon_types.append(types.type.name)
        except:
            print('[ERROR] Could not get pokemon types')
    
        return pokemon_types

    def get_damage_relations( self, type ):
        damage_relations = self.client.get_type(type)[0].damage_relations
        
        # dd_relation = damage_relations.double_damage_from
        double_damage_from = []
        for rel in damage_relations.double_damage_from:
            double_damage_from.append(rel.name)
            
        # hd_relation = damage_relations.half_damage_from
        half_damage_from = []
        for rel in damage_relations.half_damage_from:
            half_damage_from.append(rel.name)
        
        # nd_relation = damage_relations.no_damage_from
        no_damage_from = []
        for rel in  damage_relations.no_damage_from:
            no_damage_from.append(rel.name)
        
        damage_relations = {}
        damage_relations["type"] = type
        damage_relations["double_damage_from"] = double_damage_from
        damage_relations["half_damage_from"] = half_damage_from
        damage_relations["no_damage_from"] = no_damage_from
        
        return damage_relations
        
    def get_pokemon_stats( self, db_pokemon ):
        stats = []
        
        for stat in db_pokemon.stats:
            stats.append({stat.stat.name: stat.base_stat})
            
        return stats