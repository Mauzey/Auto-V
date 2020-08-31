# import modules
from vehicle import Vehicle
from utils import process_image, debug_overlay

from PIL import ImageGrab

import numpy as np
import time
import cv2


if __name__ == '__main__':
    # init car and debug
    car = Vehicle()
    
    debug_info = {
        'frame_time': '',
        }
    
    last_time = time.time()
    
    # main loop
    while(True):
        # capture the top left corner (800x640px) of the screen
        raw_screen = np.array(ImageGrab.grab(bbox=(0, 40, 800, 640)))
        
        last_time = time.time()
        
        # process the captured screen
        processed_screen = process_image(raw_screen)
        
        # time taken to process the frame
        debug_info['frame_time'] = round(time.time() - last_time, 5)
        
        # print debug overlay
        debug_screen = debug_overlay(processed_screen, debug_info)
        
        # show screen
        cv2.imshow('Auto V', debug_screen)
        
        # process user input
        keypress = cv2.waitKey(25)
        
        if keypress & 0xFF == ord('q'):
            # quit application
            cv2.destroyAllWindows()
            break