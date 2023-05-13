from src.Database_service import Database_service as db
from src.util import Util
import pokebase


def main():
    # list = db.get_pokemon_types("oddish")
    
    # print(list)
    util = Util()
    # hwnd = util.find_window()
    util.capture_screen(True, True, False)
    

if __name__ == '__main__':
    main()