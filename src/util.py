import win32gui
import numpy as np
import cv2
from mss import mss
from PIL import Image         
            
class Util():
    def __init__(self):
        self.window_handle = 0
        self.sct = mss()
        self.bounding_box = {}
        
    
    def capture_screen( self ):
        while True:
            
            window_rect = win32gui.GetWindowRect( self.find_window() )
        
            window_width = abs(window_rect[0]) - abs(window_rect[2])
            window_height = abs(window_rect[3]) - abs(window_rect[1])
            
            print(f'width: {window_width} = {window_rect[2]} - {window_rect[0]}')
            print(f'height: {window_height} = {window_rect[3]} - {window_rect[1]}')
            
            self.bounding_box = {'top': window_rect[1], 'left': window_rect[0], 'width': abs(window_width), 'height': abs(window_height)}
            
            sct_img = self.sct.grab(self.bounding_box)
            cv2.imshow('screen', np.array(sct_img))
            
            if (cv2.waitKey(1) & 0xFF) == ord('q'):
                cv2.destroyAllWindows()
                break
    
    
    def find_window(self) -> int:
        win32gui.EnumWindows( self.winEnumHandler, None )
        
        return self.window_handle


    def winEnumHandler( self, hwnd, ctx ):
            window_text = win32gui.GetWindowText( hwnd ).lower()
            if 'pokemmo' == window_text:#win32gui.IsWindowVisible( hwnd ) and 
                print ( hex( hwnd ), win32gui.GetWindowText( hwnd ) )
                self.window_handle = hwnd
        