C:\Users\mzoodias\Desktop\cht>python main.py
Traceback (most recent call last):
  File "C:\Users\mzoodias\Desktop\cht\main.py", line 21, in <module>
    points = vision_stone.find(screenshot, 0.5, 'rectangles')
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\mzoodias\Desktop\cht\vision.py", line 24, in find
    result = cv.matchTemplate(icestone_img, self.needle_img, self.method)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
cv2.error: OpenCV(4.9.0) D:\a\opencv-python\opencv-python\opencv\modules\imgproc\src\templmatch.cpp:1164: error: (-215:Assertion failed) (depth == CV_8U || depth == CV_32F) && type == _templ.type() && _img.dims() <= 2 in function 'cv::matchTemplate'
