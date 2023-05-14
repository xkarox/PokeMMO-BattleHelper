from src.Database_service import Database_service
from src.game_data_service import game_data_service
import keyboard

import cv2

def main():
    gds = game_data_service()
    db = Database_service()

    window_handle = gds.find_window()
    while True:
        if (keyboard.is_pressed("9")):
            print("Key pressed")
            img = gds.capture_screen( window_handle, showWindow=False)
            data = gds.process_image(img)
            found_pokemon = gds.find_pokemon_names(data)

            print(f'Found pokemon: {len(found_pokemon)}')
            
            if len(found_pokemon) != 0:
            
                for pokemon in found_pokemon:

                    db_pokemon = db.get_pokemon(pokemon)
                    types = db.get_pokemon_types(db_pokemon)
                    
                    print(f'Pokemon: {db_pokemon}\nTypes: {types}')
            
            #close the window when pressing 'q'      
            if (cv2.waitKey(1) & 0xFF) == ord('q'):
                cv2.destroyAllWindows()
                break

if __name__ == '__main__':
    main()