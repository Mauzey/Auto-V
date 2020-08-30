# import modules
from PIL import ImageGrab

import numpy as np
import cv2
import time

def process_img(image):
    """
    
    """
    
    # convert to greyscale
    grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # edge detection
    edge_image = cv2.Canny(grey_image, threshold1=200, threshold2=300)
    
    return edge_image

def main():
    last_time = time.time()
    
    while True:
        # capture top left corner (800x640px) of the screen
        raw_screen = np.array(ImageGrab.grab(bbox=(0, 40, 800, 640)))
        
        #print('loop took {} seconds'.format(time.time() - last_time))
        
        last_time = time.time()
        
        # process captured screen and show it
        new_screen = process_img(raw_screen)
        cv2.imshow('window', new_screen)
        
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

main()