import cv2 as cv
import numpy as np
import os
from time import time
from windowcapture import WindowCapture
from PIL import ImageGrab
from vision import Vision
from hsvfilter import HsvFilter


os.chdir(os.path.dirname(os.path.abspath(__file__)))


wincap = WindowCapture('Astra2')


vision_stone = Vision('ice_stone.jpg')

vision_stone.init_control_gui()  # nem volt

#hsv_filter = HsvFilter(0,0,0,91,255,255,0,0,0,0)

loop_time = time()
while(True):

    screenshot = wincap.get_screenshot()
    
    processed_image = vision_stone.apply_hsv_filter(screenshot) #   hsv_filter

    rectangles = vision_stone.find(processed_image, 0.5, debug_mode=None )  # points = .....'                 (screenshot, 0.5, 'rectangles')
    
    
    output_image = vision_stone.draw_rectangles(screenshot, rectangles)   # ez sem volt ittt
    
    cv.imshow('Matches', output_image) 
    cv.imshow('Matches2', processed_image)
    
    
    #print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()


    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')