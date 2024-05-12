import os
import time
from threading import Thread

import cv2
from dotenv import load_dotenv
from urllib.parse import urljoin

load_dotenv()

WEBCAM_USER = os.environ.get("WEBCAM_USER")
WEBCAM_PASSWORD = os.environ.get("WEBCAM_PASSWORD")
IP = os.environ.get("IP")
PORT = os.environ.get("PORT")
WEBCAM_BASE_URL = f"http://{WEBCAM_USER}:{WEBCAM_PASSWORD}@{IP}:{PORT}/"

thres = 0.45  # Threshold to detect object

##############cv2 property parameters (optional)############################
# 0. CV_CAP_PROP_POS_MSEC Current position of the video file in milliseconds.
# 1. CV_CAP_PROP_POS_FRAMES 0-based index of the frame to be decoded/captured next.
# 2. CV_CAP_PROP_POS_AVI_RATIO Relative position of the video file
# 3. CV_CAP_PROP_FRAME_WIDTH Width of the frames in the video stream.
# 4. CV_CAP_PROP_FRAME_HEIGHT Height of the frames in the video stream.
# 5. CV_CAP_PROP_FPS Frame rate.
# 6. CV_CAP_PROP_FOURCC 4-character code of codec.
# 7. CV_CAP_PROP_FRAME_COUNT Number of frames in the video file.
# 8. CV_CAP_PROP_FORMAT Format of the Mat objects returned by retrieve() .
# 9. CV_CAP_PROP_MODE Backend-specific value indicating the current capture mode.
# 10. CV_CAP_PROP_BRIGHTNESS Brightness of the image (only for cameras).
# 11. CV_CAP_PROP_CONTRAST Contrast of the image (only for cameras).
# 12. CV_CAP_PROP_SATURATION Saturation of the image (only for cameras).
# 13. CV_CAP_PROP_HUE Hue of the image (only for cameras).
# 14. CV_CAP_PROP_GAIN Gain of the image (only for cameras).
# 15. CV_CAP_PROP_EXPOSURE Exposure (only for cameras).
# 16. CV_CAP_PROP_CONVERT_RGB Boolean flags indicating whether images should be converted to RGB.
# 17. CV_CAP_PROP_WHITE_BALANCE Currently unsupported
# 18. CV_CAP_PROP_RECTIFICATION Rectification flag for stereo cameras (note: only supported by DC1394 v 2.x backend currently)
##############################################################################################################################


class ThreadedCamera(object):
    def __init__(self, web=False, src=0):
        if web:
            self.source = urljoin(WEBCAM_BASE_URL, "video")
        else:
            self.source = src
        self.capture = cv2.VideoCapture(self.source)
        self.capture.set(3, 640)  # set width of the frame
        self.capture.set(4, 480)  # set height of the frame
        # self.capture.set(10, 70)  # set image brightness
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)
       
        # FPS = 1/X
        # X = desired FPS
        self.FPS = 1/30
        self.FPS_MS = int(self.FPS * 1000)
        
        # Start frame retrieval thread
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        
    def update(self):
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
                # result, objectInfo = getObjects(self.frame, objects=['remote'])
                # print(objectInfo)
                ## Drawing the lines
                # cv2.line(self.frame, (0, 0), (640, 480), (0, 0, 255), 5)
                # cv2.line(self.frame, (640, 0), (0, 480), (0, 0, 255), 5)
            time.sleep(self.FPS)
            
    def show_frame(self):
        # screen = cv2.resize(self.frame, (960, 540))
        # cv2.imshow('Output', screen)
        cv2.imshow('Output', self.frame)
        cv2.waitKey(self.FPS_MS)
        
    def screenshot(self):
        while True:
            success, img = self.capture.read()
            if success:
                cv2.imwrite("now.png", img)
            cv2.destroyAllWindows()
                

def main():
    threaded_camera = ThreadedCamera(web=True)

    while True:
        try:
            threaded_camera.screenshot()
            break

        except AttributeError:
            pass


if __name__ == '__main__':
    main()
