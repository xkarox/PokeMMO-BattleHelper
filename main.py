from src.Database_service import Database_service
from src.game_data_service import game_data_service
import pokebase


def main():
    # list = db.get_pokemon_types("oddish")
    
    # print(list)
    gds = game_data_service()
    # db = Database_service()
    # gastly = db.get_pokemon("gastly")
    
    # print(gastly)
    # print(type(gastly))
    
    # print(db.get_pokemon_types(gastly))
    
    gds.capture_screen()
    

if __name__ == '__main__':
    main()