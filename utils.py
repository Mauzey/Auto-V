# import modules
import numpy as np
import cv2

def debug_overlay(frame, debug_info):
    # parameters
    font = cv2.FONT_HERSHEY_PLAIN
    font_scale = 1
    font_color = (0, 0, 0)
    rect_color = (255, 255, 255)
    line_type = 1
    position = (10, 585)
    
    # print background rectangles
    for i,(x, y) in enumerate(debug_info.items()):
        cv2.rectangle(frame,
                      (position[0], position[1] - (i * 15) - 13),
                      (position[0] + 200, position[1] - (i * 15) + 2),
                      rect_color, -1)
    
    # print debug information
    for i, (x, y) in enumerate(debug_info.items()):
        cv2.putText(frame, x + ': ' + str(y),
                    (position[0], position[1] - (i * 15)),
                    font, font_scale, font_color, line_type)
    
    return frame