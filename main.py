from src.Database_service import Database_service
from src.game_data_service import game_data_service
import keyboard

import cv2

def main():
    # list = db.get_pokemon_types("oddish")
    
    # print(list)
    gds = game_data_service()
    db = Database_service()
    # gastly = db.get_pokemon("gastly")
    
    # print(gastly)
    # print(type(gastly))
    
    # print(db.get_pokemon_types(gastly))
    
    window_handle = gds.find_window()
    while True:
        if (keyboard.is_pressed("9")):
            print("pressed")
            img = gds.capture_screen( window_handle, showWindow=False)
            data = gds.process_image(img)
            found_pokemon = gds.find_pokemon_names(data)
            # found_pokemon = ['oddish', 'gastly', 'starmie']
            # if len(found_pokemon) != 0:
            print(len(found_pokemon))
            for pokemon in found_pokemon:
                # gastly = db.get_pokemon("oddish")
                db_pokemon = db.get_pokemon(pokemon)
                types = db.get_pokemon_types(db_pokemon)
                print(f'Pokemon: {db_pokemon}\nTypes: {types}')
            
            #close the window when pressing 'q'      
            if (cv2.waitKey(1) & 0xFF) == ord('q'):
                cv2.destroyAllWindows()
                break

if __name__ == '__main__':
    main()