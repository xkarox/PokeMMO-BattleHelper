from src.Database_service import Database_service
from src.game_data_service import game_data_service
import keyboard
from colorama import init as colorama_init
from colorama import Fore
from colorama import Back
from colorama import Style
import cv2

def main():

    colorama_init()
    
    gds = game_data_service()
    db = Database_service()

    window_handle = gds.find_window()
    while True:
        if (keyboard.is_pressed("9")):
        # if(True):
            print("Key pressed")
            
            img = gds.capture_screen( window_handle, showWindow=False)
            data = gds.process_image(img)
            found_pokemon = gds.find_pokemon_names(data)

            print(f'Found pokemon: {len(found_pokemon)}')
            
            if len(found_pokemon) != 0:
                #iterate through all pokemon found on screen
                for pokemon in found_pokemon:

                    db_pokemon = db.get_pokemon(pokemon)
                    types = db.get_pokemon_types(db_pokemon)
                    
                    #iterate thorugh all types of the found pokemon
                    damage_relations = []
                    for type in types: 
                        damage_relations.append(db.get_damage_relations(type))
                        
                        
                    print(f'\n\nPokemon: {db_pokemon.name}\nTypes: {types}')
                    
                    for relation in damage_relations:
                        print(f'\n{Back.BLACK}{Fore.RED}relation.double_damage_from:{Style.RESET_ALL}')
                        for rel in relation.double_damage_from:
                            print(f'    {rel.name}{Style.RESET_ALL}')
                            
                        print(f'\n{Back.BLACK}{Fore.YELLOW}relation.half_damage_from:{Style.RESET_ALL}')    
                        for rel in relation.half_damage_from:
                            print(f'    {rel.name}{Style.RESET_ALL}')
                        
                        print(f'\n{Back.BLACK}{Fore.GREEN}relation.no_damage_from:{Style.RESET_ALL}')
                        for rel in relation.no_damage_from:
                            print(f'    {rel.name}{Style.RESET_ALL}')
                        
            #close the window when pressing 'q'      
            if (cv2.waitKey(1) & 0xFF) == ord('q'):
                cv2.destroyAllWindows()
                break
        
        
if __name__ in {"__main__", "__mp_main__"}:
    main()