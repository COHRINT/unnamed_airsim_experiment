#!/usr/bin/env python

from flask import Flask, render_template_string, Response

import airsim
# import cv2
import numpy as np
# import rospy
# from geometry_msgs.msg import Twist
# from sensor_msgs.msg import CompressedImage
from PIL import Image
import io

client = airsim.MultirotorClient()
client.confirmConnection()

CAMERA_NAME = '0'
IMAGE_TYPE = airsim.ImageType.Scene
DECODE_EXTENSION = '.jpg'

# rospy.init_node('video_stream')
# image_pub = rospy.Publisher("/%s/output/image_raw/compressed" % self.name, CompressedImage)
# subscriber = rospy.Subscriber("/camera/image/compressed",
#     CompressedImage, callback,  queue_size = 1)
#
# def callback(data):
#     np_response_image = np.fromstring(data.data, np.uint8)
#     decoded_frame = cv2.imdecode(np_response_image, cv2.IMREAD_COLOR)
#     ret, encoded_jpeg = cv2.imencode(DECODE_EXTENSION, decoded_frame)
#     frame = encoded_jpeg.tobytes()
#     # Return Decoded Image
#     yield (b'--frame\r\n'
#            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
def frame_generator():
    while (True):
        # Get Image
        response_image = client.simGetImage(CAMERA_NAME, IMAGE_TYPE)
        np_response_image = np.asarray(bytearray(response_image), dtype="uint8")
        # Publish to ROS

        # Decode Image
        # decoded_frame = cv2.imdecode(np_response_image, cv2.IMREAD_COLOR)
        # ret, encoded_jpeg = cv2.imencode(DECODE_EXTENSION, decoded_frame)
        # frame = encoded_jpeg.tobytes()
        # image = Image.frombytes("RGB", (1280, 720), np_response_image)
        # imgByteArr = io.BytesIO()
        # image.save(imgByteArr, format='JPEG')
        # imgByteArr = imgByteArr.getvalue()
        # frame = imgByteArr
        frame = np_response_image

        # Return Decoded Image
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string(
        """
            <html>
            <head>
                <title>AirSim Streamer</title>
            </head>
            <body>
                <h1>AirSim Streamer</h1>
                <hr />
                <a href="/video_feed">http://localhost:5000/video_feed</a>
            </body>
            </html>
        """
        )

@app.route('/video_feed')
def video_feed():
    return Response(
            frame_generator(),
            mimetype='multipart/x-mixed-replace; boundary=frame'
        )



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
