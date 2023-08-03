import os

import numpy as np
import cv2
# from alerts.alarm_sounds.audioplaybackbg import *


root = os.getcwd()

class CameraTampering:

    def __init__(self, camera_tamper_queue, fgbg):

        self.camera_tamper_queue = camera_tamper_queue
        self.fgbg = fgbg
        self.kernel = np.ones((5, 5), np.uint8)

    def frame_process(self, frame):

        fgmask = self.fgbg.apply(frame)
        fgmask = cv2.erode(fgmask, self.kernel, iterations=5)
        fgmask = cv2.dilate(fgmask, self.kernel, iterations=5)
        contours, _ = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        bounding_rect = [cv2.boundingRect(contour) for contour in contours]
        a = sum(rect[2] * rect[3] for rect in bounding_rect if rect[2] >= 40 or rect[3] >= 40)
        if a != 307200:
            return a
        else:
            return None

    def detect(self):

        frame = self.camera_tamper_queue.get()

        try:
            print("Initiating Camera Tampering Detection...")

            a = self.frame_process(frame)
            if a is not None:
                if a >= int(frame.shape[0]) * int(frame.shape[1]) / 3:

                    cv2.putText(frame, "TAMPERING DETECTED", (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                return frame
            else:
                return frame
        except Exception as ex:
            print("Error occurred while detecting camera tampering {}".format(ex))
            return frame


