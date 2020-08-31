# import modules
import numpy as np
import cv2

def draw_lines(image, lines):
    for line in lines:
        coords = line[0]
        cv2.line(image, (coords[0], coords[1]), (coords[2], coords[3]), [255, 255, 255], 3)

def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
    
    # apply automatic canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 - sigma) * v))
    
    return cv2.Canny(image, lower, upper)

def process_image(image):
    # convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # apply gaussian blur
    blur_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    
    # perform edge detection
    #edge_image = cv2.Canny(blur_image, 100, 200)
    edge_image = auto_canny(blur_image)
    
    # crop region of interest
    vertices = np.array([(10, 500), (10, 300), (300, 200), (500, 200), (800, 300), (800, 500)])
    roi_mask = np.zeros_like(edge_image)
    cv2.fillPoly(roi_mask, np.array([vertices], dtype=np.int32), 255)
    masked_image = cv2.bitwise_and(edge_image, roi_mask)
    
    # use hough lines to find dominant lines within the image
    lines = cv2.HoughLinesP(masked_image, rho=1, theta=np.pi/180, threshold=10,
                            lines = np.array([]), minLineLength=8, maxLineGap=4)
    draw_lines(masked_image, lines)
    
    return masked_image

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