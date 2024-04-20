import cv2 as cv
import numpy as np

from hsvfilter import HsvFilter


class Vision:
    # constant
    TRACKBAR_WINDOW = 'Trackbars'
    
    
    needle_img = None
    needle_w = 0
    needle_h = 0
    method = None



    def __init__(self, needle_img_path, method=cv.TM_CCOEFF_NORMED):
        self.needle_img = cv.imread(needle_img_path)  #cv.IMREAD_UNCHANGED


        self.needle_w = self.needle_img.shape[1]
        self.needle_h = self.needle_img.shape[0]

        self.method = method


    def find(self, icestone_img, threshold=0.5, max_results=10, debug_mode=None):   #debug_mode=None,  # max_results=10
        
        
        #### SZÜRKÉVÉ VÁLTOZTATÁS -----------------------------  
        """"

        icestone_img = cv.cvtColor(icestone_img, cv.COLOR_BGR2GRAY)

 
        needle_resized = cv.cvtColor(needle_resized, cv.COLOR_BGR2GRAY)

        
        # SZÜRKÉVÉ VÁLTOZTATÁS VÉGE ------------------------------ 
        """
        
        
        needle_resized = cv.resize(self.needle_img, (self.needle_w, self.needle_h))

 
        result = cv.matchTemplate(icestone_img, needle_resized, self.method)


     
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        if not locations:
           return np.array([], dtype=np.int32).reshape(0, 4)

       
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_w, self.needle_h]
            rectangles.append(rect)
            rectangles.append(rect)

        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

        return rectangles
    
    
        if len(rectangles) > max_results:
           print('Warning: too many results, raise the threshold.')
           rectangles = rectangles[:max_results]

        return rectangles
    
        if debug_mode:
      
            if debug_mode == 'rectangles':
                for (x, y, w, h) in rectangles:
                    cv.rectangle(icestone_img, (x, y), (x+w, y+h), (0, 255, 0), 2)

 
            elif debug_mode == 'points':
                for point in points:
                    cv.drawMarker(icestone_img, point, (0, 255, 0), cv.MARKER_CROSS, 40, 2)

 
            cv.imshow('Matches', icestone_img)

        return points
    
    
    
    def get_click_points(self, rectangles):
            points = []

            # Loop over all the rectangles
            for (x, y, w, h) in rectangles:
                # Determine the center position
                center_x = x + int(w/2)
                center_y = y + int(h/2)
                # Save the points
                points.append((center_x, center_y))

            return points



  #  INNENTÖL NEM VOLTAK -------------------------------------------------------------
  
    def draw_rectangles(self, icestone_img, rectangles):
        # these colors are actually BGR
        line_color = (0, 255, 0)
        line_type = cv.LINE_4

        for (x, y, w, h) in rectangles:
            # determine the box positions
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            # draw the box
            cv.rectangle(icestone_img, top_left, bottom_right, line_color, lineType=line_type)

        return icestone_img

    # given a list of [x, y] positions and a canvas image to draw on, return an image with all
    # of those click points drawn on as crosshairs
    def draw_crosshairs(self, icestone_img, points):
        # these colors are actually BGR
        marker_color = (255, 0, 255)
        marker_type = cv.MARKER_CROSS

        for (center_x, center_y) in points:
            # draw the center point
            cv.drawMarker(icestone_img, (center_x, center_y), marker_color, marker_type)

        return icestone_img

    # create gui window with controls for adjusting arguments in real-time
    def init_control_gui(self):
        cv.namedWindow(self.TRACKBAR_WINDOW, cv.WINDOW_NORMAL)
        cv.resizeWindow(self.TRACKBAR_WINDOW, 350, 700)

        # required callback. we'll be using getTrackbarPos() to do lookups
        # instead of using the callback.
        def nothing(position):
            pass

        # create trackbars for bracketing.
        # OpenCV scale for HSV is H: 0-179, S: 0-255, V: 0-255
        cv.createTrackbar('HMin', self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar('SMin', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VMin', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('HMax', self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar('SMax', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VMax', self.TRACKBAR_WINDOW, 0, 255, nothing)
        # Set default value for Max HSV trackbars
        cv.setTrackbarPos('HMax', self.TRACKBAR_WINDOW, 179)
        cv.setTrackbarPos('SMax', self.TRACKBAR_WINDOW, 255)
        cv.setTrackbarPos('VMax', self.TRACKBAR_WINDOW, 255)

        # trackbars for increasing/decreasing saturation and value
        cv.createTrackbar('SAdd', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('SSub', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VAdd', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VSub', self.TRACKBAR_WINDOW, 0, 255, nothing)

    # returns an HSV filter object based on the control GUI values
    def get_hsv_filter_from_controls(self):
        # Get current positions of all trackbars
        hsv_filter = HsvFilter()
        hsv_filter.hMin = cv.getTrackbarPos('HMin', self.TRACKBAR_WINDOW)
        hsv_filter.sMin = cv.getTrackbarPos('SMin', self.TRACKBAR_WINDOW)
        hsv_filter.vMin = cv.getTrackbarPos('VMin', self.TRACKBAR_WINDOW)
        hsv_filter.hMax = cv.getTrackbarPos('HMax', self.TRACKBAR_WINDOW)
        hsv_filter.sMax = cv.getTrackbarPos('SMax', self.TRACKBAR_WINDOW)
        hsv_filter.vMax = cv.getTrackbarPos('VMax', self.TRACKBAR_WINDOW)
        hsv_filter.sAdd = cv.getTrackbarPos('SAdd', self.TRACKBAR_WINDOW)
        hsv_filter.sSub = cv.getTrackbarPos('SSub', self.TRACKBAR_WINDOW)
        hsv_filter.vAdd = cv.getTrackbarPos('VAdd', self.TRACKBAR_WINDOW)
        hsv_filter.vSub = cv.getTrackbarPos('VSub', self.TRACKBAR_WINDOW)
        return hsv_filter

    # given an image and an HSV filter, apply the filter and return the resulting image.
    # if a filter is not supplied, the control GUI trackbars will be used
    def apply_hsv_filter(self, original_image, hsv_filter=None):
        # convert image to HSV
        hsv = cv.cvtColor(original_image, cv.COLOR_BGR2HSV)

        # if we haven't been given a defined filter, use the filter values from the GUI
        if not hsv_filter:
            hsv_filter = self.get_hsv_filter_from_controls()

        # add/subtract saturation and value
        h, s, v = cv.split(hsv)
        s = self.shift_channel(s, hsv_filter.sAdd)
        s = self.shift_channel(s, -hsv_filter.sSub)
        v = self.shift_channel(v, hsv_filter.vAdd)
        v = self.shift_channel(v, -hsv_filter.vSub)
        hsv = cv.merge([h, s, v])

        # Set minimum and maximum HSV values to display
        lower = np.array([hsv_filter.hMin, hsv_filter.sMin, hsv_filter.vMin])
        upper = np.array([hsv_filter.hMax, hsv_filter.sMax, hsv_filter.vMax])
        # Apply the thresholds
        mask = cv.inRange(hsv, lower, upper)
        result = cv.bitwise_and(hsv, hsv, mask=mask)

        # convert back to BGR for imshow() to display it properly
        img = cv.cvtColor(result, cv.COLOR_HSV2BGR)

        return img

    # apply adjustments to an HSV channel
    # https://stackoverflow.com/questions/49697363/shifting-hsv-pixel-values-in-python-using-numpy
    def shift_channel(self, c, amount):
        if amount > 0:
            lim = 255 - amount
            c[c >= lim] = 255
            c[c < lim] += amount
        elif amount < 0:
            amount = -amount
            lim = amount
            c[c <= lim] = 0
            c[c > lim] -= amount
        return c


    
            




        # IDÁIG NEMVOLTAK ----------------------------------------------------------------------


"""        if debug_mode:
      
            if debug_mode == 'rectangles':
                for (x, y, w, h) in rectangles:
                    cv.rectangle(icestone_img, (x, y), (x+w, y+h), (0, 255, 0), 2)

 
            elif debug_mode == 'points':
                for point in points:
                    cv.drawMarker(icestone_img, point, (0, 255, 0), cv.MARKER_CROSS, 40, 2)

 
            cv.imshow('Matches', icestone_img)

        return points"""
        
