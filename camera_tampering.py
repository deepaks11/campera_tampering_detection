import numpy as np
import cv2,os
# from alerts.alarm_sounds.audioplaybackbg import *

kernel = np.ones((5, 5), np.uint8)
root = os.getcwd()


def cam_tampering_main(camera_tamper_queue, fgbg):
    frame = camera_tamper_queue.get()
    cam_tampering_flag = False
    im = frame.copy()
    try:
        # trace.info("Initiating Camera Tampering Detection...")
        a = 0
        bounding_rect = []
        fgmask = fgbg.apply(frame)
        fgmask = cv2.erode(fgmask, kernel, iterations=5)
        fgmask = cv2.dilate(fgmask, kernel, iterations=5)
        contours, _ = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # position = (545, 25)
        # cv2.putText(frame, "Camera Tampering Detection", position, cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
        for i in range(0, len(contours)):
            bounding_rect.append(cv2.boundingRect(contours[i]))
        for i in range(0, len(contours)):
            bounding_rect[i][2] >= 40 or bounding_rect[i][3] >= 40
            a = a + (bounding_rect[i][2]) * bounding_rect[i][3]
            if (a >= int(frame.shape[0]) * int(frame.shape[1]) / 3):
                cv2.putText(frame, "TAMPERING DETECTED", (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cam_tampering_flag = True

        return frame, cam_tampering_flag
    except Exception as ex:
        # exc.exception("Error occurred while detecting camera tampering {}".format(ex))
        return frame, cam_tampering_flag
