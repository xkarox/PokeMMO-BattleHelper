import win32gui
import numpy as np
import cv2
import pytesseract
import time 
from mss import mss
from PIL import Image
            
class Util():
    def __init__(self):
        self.window_handle = 0
        self.sct = mss()
        self.bounding_box = {}
        pytesseract.pytesseract.tesseract_cmd = 'F:\\Tesseract\\tesseract.exe'
        
    def process_image( self, image ):

        img = np.array(image)
        # Grayscale, Gaussian blur, Otsu's threshold
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3,3), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Morph open to remove noise and invert image
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)
        invert = 255 - opening
        
        # Perform text extraction
        data = pytesseract.image_to_string(invert, config='--psm 6')
        print(data)
        
        # cv2.imshow('thresh', thresh)
        # cv2.imshow('opening', opening)
        # cv2.imshow('invert', invert)
        
        return data
        
    def set_bounding_box( self ):
        window_handle = self.find_window()
        window_rect = win32gui.GetWindowRect( window_handle )
        
        window_width = abs(window_rect[0]) - abs(window_rect[2])
        window_height = abs(window_rect[3]) - abs(window_rect[1])
        
        window_width = abs(window_width)
        window_height = abs(window_height)

        self.bounding_box = {'top': int(window_rect[1]), 'left': int(window_rect[0]) , 'width': int(window_width) , 'height': int(window_height) }
            
    def find_window(self) -> int:
        win32gui.EnumWindows( self.winEnumHandler, None )
        
        return self.window_handle

    def winEnumHandler( self, hwnd, ctx ):
            window_text = win32gui.GetWindowText( hwnd ).lower()
            
            if 'pokemmo' == window_text or 'pokеммo' == window_text or 'рokemмo' == window_text or 'pokeмmo' == window_text:# and win32gui.IsWindowVisible( hwnd ):
                print ( hex( hwnd ), window_text )
                self.window_handle = hwnd
                
    #asnyc dis method to make the programm run faster 
    def capture_screen( self, showWindow: bool = False , showFps: bool = False, showBoxes: bool = False):
        
        begin_time = time.time()
        frames = 0
        
        while True:
            self.set_bounding_box()
            sct_img = self.sct.grab(self.bounding_box)
            img = np.array(sct_img)
            data, contours = self.process_image(sct_img)
            
            if showFps: 
                frames += 1
                fps = frames / (time.time() - begin_time)
                
                cv2.putText(img, str(fps), (7, 70), cv2.FONT_HERSHEY_PLAIN, 3, (100, 255, 0), 3, cv2.LINE_AA)
                # print(f'FPS: {fps}')
                    
            if showWindow:
                cv2.imshow('screen', img)
                  
            if (cv2.waitKey(1) & 0xFF) == ord('q'):
                cv2.destroyAllWindows()
                break
            
            