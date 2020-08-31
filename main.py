# import modules
from lane_detector import LaneDetector
from vehicle import Vehicle
from utils import debug_overlay

from PIL import ImageGrab

import numpy as np
import time
import cv2


if __name__ == '__main__':
    # init car and lane detector objects
    car = Vehicle()
    lane_detector = LaneDetector()
    
    debug_info = {
        'frame_time': '',
        'steering_angle': 0.5,
        'throttle_value': 0
        }
    
    last_time = time.time()
    
    # main loop
    while(True):
        # capture the top left corner (800x640px) of the screen
        raw_screen = np.array(ImageGrab.grab(bbox=(0, 40, 800, 640)))
        
        last_time = time.time()
        
        # process the captured screen
        processed_screen = lane_detector.detect_lanes(raw_screen)
        car.set_axis('steering_angle', lane_detector.calculate_steering_angle(processed_screen))
        debug_info['steering_angle'] = car.axis['steering_angle']
        
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
        elif keypress & 0xFF == ord('5'):
            # toggle car's throttle
            if car.axis['throttle_value'] == 0:
                car.set_axis('throttle_value', 0.5)
            else:
                car.set_axis('throttle_value', 0)
            
            debug_info['throttle_value'] = car.axis['throttle_value']