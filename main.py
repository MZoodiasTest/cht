import cv2 as cv
import numpy as np
import os
from time import time
from windowcapture import WindowCapture
from vision import Vision
from PIL import ImageGrab

os.chdir(os.path.dirname(os.path.abspath(__file__)))


wincap = WindowCapture('Astra2')
vision_stone = Vision('ice_stone.jpg')


loop_time = time()
while(True):

    screenshot = wincap.get_screenshot()

    points = vision_stone.find(screenshot, 0.5, 'rectangles')

    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()


    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')