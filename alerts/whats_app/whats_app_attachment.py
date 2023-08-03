import cv2
from processor.logger import exc
import base64
import urllib.parse as up
from datetime import datetime
import threading
import requests

# current dateTime
now = datetime.now()
# convert to string
date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")


def whatsapp_notification(tress_image_path, token, to_number, instance, cam_name, use_case):
    try:
        cur_date_time = datetime.now()
        # convert to string
        date_time_string = cur_date_time.strftime("%Y-%m-%d %H:%M:%S")
        error = f"{use_case} occur on {cam_name} in {date_time_string}"
        img = cv2.imread(tress_image_path)
        jpg_img = cv2.imencode('.jpeg', img)
        b64_string = base64.b64encode(jpg_img[1]).decode('utf-8')
        img_txt_encoded = up.quote_plus(b64_string)
        sub = img_txt_encoded
        tokens = token
        to = to_number
        url = f"https://api.ultramsg.com/f{instance}/messages/image"
        payload = f"token={tokens}&to={to}&image={sub}&caption={error} &referenceId=&nocache="
        # payload1 = f"token={tokens}&to={to}&video={sub1}&caption={error}&referenceId=&nocache="
        # payload = f"token={tokens}&t0={to}&body={sub}&caption=image Caption&referenceId=&nocache="
        # payload = "token=ju3v2m1nemzwbnn3&to=8778003972&image=https://file-example.s3-accelerate.amazonaws.com/images/test.jpg&caption=image Caption&referenceId=&nocache="
        # payload = f"token={tokens}&to={to}&body={sub}&priority=10&referenceId="
        headers = {'content-type': "application/x-www-form-urlencoded"}
        # qwe=encoders.encode_base64(payload)
        response = requests.request("POST", url, data=payload, headers=headers)
        # conn.request("POST", "/instance9090/messages/video", payload1, headers)

        data = response.read()
        print(data.decode("utf-8"))
        return data
    except Exception as ex:
        exc.exception("Error message not sent {}".format(ex))
        print(ex)


def whats_image_notification(tress_image_path, token, to_number, instance, cam_name, use_case):
    whatsapp = threading.Thread(target=whatsapp_notification, args=(tress_image_path, token, to_number, instance, cam_name, use_case))
    whatsapp.start()
