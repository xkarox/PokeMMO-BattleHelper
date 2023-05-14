import win32gui
import numpy as np
import cv2
import pytesseract
from mss import mss
import re

class game_data_service():
    def __init__( self ):
        self.window_handle = 0
        self.bounding_box = {}
        self.sct = mss()
        self.pattern = r"(\w+)\s+Lv\.\s+(\d+)"
        pytesseract.pytesseract.tesseract_cmd = 'F:\\Tesseract\\tesseract.exe'
    
    def find_window( self ):
        def winEnumHandler( hwnd: int, ctx ):
                window_text = win32gui.GetWindowText( hwnd ).lower()
                # if win32gui.IsWindowVisible( hwnd ):
                #     print ( hex( hwnd ), window_text )
                if 'pokemmo' == window_text or 'pokеммo' == window_text or 'рokemмo' == window_text or 'pokeмmo' == window_text:
                    # print ( hex( hwnd ), window_text )
                    self.window_handle = hwnd
        win32gui.EnumWindows( winEnumHandler, None )
        
        return self.window_handle
    
    def find_bounding_box( self, window_handle: int):

        window_rect = win32gui.GetWindowRect( self.window_handle )
        
        window_width = abs(window_rect[0]) - abs(window_rect[2])
        window_height = abs(window_rect[3]) - abs(window_rect[1])
        
        window_width = abs(window_width)
        window_height = abs(window_height)

        self.bounding_box = {'top': int(window_rect[1]), 'left': int(window_rect[0]), 'width': int(window_width), 'height': int(window_height)}
    
    def process_image( self, image: np.array ):
        # Grayscale, Gaussian blur, Otsu's threshold
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Morph open to remove noise and invert image
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)
        invert = 255 - opening
        
        # Perform text extraction
        data = pytesseract.image_to_string(invert, config='--psm 6')
        # print(data)
        
        return data
    
    def find_pokemon_names( self, data: str):
        found_pokemon = []
        #change pattern to also find pokemon with sex
        matches = re.findall( self.pattern, data )
        
        if matches:
            for match in matches:
                pokemon_name = match[0]
                pokemon_level = match[1]
                
                found_pokemon.append(pokemon_name)
                
        return found_pokemon    
        
                   
    def capture_screen( self, window_handle: int, showWindow: bool = False):
        #Find the bounding box 
        self.find_bounding_box( window_handle )
        
        #take a screenshot of the window and process the image
        sct_img = self.sct.grab(self.bounding_box)
        img = np.array(sct_img)
        
        #if showWindow is set to True a window showing the screenshots open
        if showWindow:
            cv2.imshow('screen', img)
        
        return img
        
            