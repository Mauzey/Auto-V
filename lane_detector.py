# import modules
import numpy as np
import cv2

class LaneDetector():
    
    def __init__(self):
        # vertices that define the region of interest
        self.roi_vertices = np.array([(10, 500), (10, 300), (300, 200),
                                      (500, 200), (800, 300), (800, 500)])
        
        # stores hough transform lines
        self.hough_lines = []
        
        print('[INFO] Lane Detector object initialised...')
    
    def detect_lanes(self, frame):
        # convert frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # apply gaussian blur
        blur_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
        
        # perform edge detection
        edge_frame = auto_canny(blur_frame)
        
        # crop region of interest
        roi_mask = np.zeros_like(edge_frame)
        cv2.fillPoly(roi_mask, np.array([self.roi_vertices], dtype=np.int32), 255)
        masked_frame = cv2.bitwise_and(edge_frame, roi_mask)
        
        # use hough transformation to find dominant lines within the image
        self.hough_lines = cv2.HoughLinesP(masked_frame, rho=1, theta=np.pi/180,
                                      threshold=10, lines=np.array([]),
                                      minLineLength=8, maxLineGap=4)
        
        # print lane markings over raw frames
        lane_markings = average_slope_intercept(frame, self.hough_lines)
        lane_frame = draw_lane_markings(frame, lane_markings)
        
        #return lane_frame
        return cv2.cvtColor(lane_frame, cv2.COLOR_BGR2RGB)



def auto_canny(frame, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(frame)
    
    # apply automatic canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 - sigma) * v))
    
    return cv2.Canny(frame, lower, upper)

def average_slope_intercept(frame, lines):
    frame_width = frame.shape[1]
    lane_markings = []
    
    # lists to store lines
    l_fit = []
    r_fit = []
    
    # if no lane markings are found
    if lines is None:
        return lane_markings
    
    # each lane marking should be in their respective (left/right) third of the screen
    boundary = 1/3
    l_region_boundary = frame_width * (1 - boundary)
    r_region_boundary = frame_width * boundary
    
    for line in lines:
        for x1, y1, x2, y2 in line:
            # skip vertical lines
            if x1 == x2:
                continue
            
            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = fit[0]
            intercept = fit[1]
            
            # determine the appropriate region for the line
            if slope < 0:
                if x1 < l_region_boundary and x2 < l_region_boundary:
                    l_fit.append((slope, intercept))
            else:
                if x1 > r_region_boundary and x2 > r_region_boundary:
                    r_fit.append((slope, intercept))
    
    # add lines to lane markings list
    l_fit_avg = np.average(l_fit, axis=0)
    if len(l_fit) > 0:
        lane_markings.append(get_endpoints(frame, l_fit_avg))
    
    r_fit_avg = np.average(r_fit, axis=0)
    if len(r_fit) > 0:
        lane_markings.append(get_endpoints(frame, r_fit_avg))
    
    return lane_markings

def get_endpoints(frame, line):
    height = frame.shape[0]
    width = frame.shape[1]
    
    slope, intercept = line
    
    y1 = height
    y2 = int(y1 * 1/2)
    
    x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
    x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
    
    return [[x1, y1, x2, y2]]

def draw_lane_markings(frame, lines, line_color=(0, 255, 0), line_width=2):
    line_frame = np.zeros_like(frame)
    
    # draw detected lane markings
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_frame, (x1, y1), (x2, y2), line_color, line_width)
    
    return cv2.addWeighted(frame, 0.8, line_frame, 1, 1)