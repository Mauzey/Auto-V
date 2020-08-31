# import modules
import cv2

def process_image(image):
    # convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # apply gaussian blur
    blur_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    
    # perform edge detection
    edge_image = cv2.Canny(blur_image, 300, 200)
    
    return edge_image

def debug_overlay(image, debug_info):
    # parameters
    font = cv2.FONT_HERSHEY_PLAIN
    font_scale = 1
    font_color = (0, 0, 0)
    rect_color = (255, 255, 255)
    line_type = 1
    position = (10, 585)
    
    # print background rectangles
    for i,(x, y) in enumerate(debug_info.items()):
        cv2.rectangle(image,
                      (position[0], position[1] - (i * 15) - 13),
                      (position[0] + 200, position[1] - (i * 15) + 2),
                      rect_color, -1)
    
    # print debug information
    for i, (x, y) in enumerate(debug_info.items()):
        cv2.putText(image, x + ': ' + str(y),
                    (position[0], position[1] - (i * 15)),
                    font, font_scale, font_color, line_type)
    
    return image