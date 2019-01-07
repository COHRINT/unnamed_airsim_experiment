#!/usr/bin/env python
import os
import io
import threading
import cv2
from PIL import Image
import numpy as np
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import CompressedImage
from flask import Flask, render_template_string, Response

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

def callback(data):
    np_response_image = np.fromstring(data.data, np.uint8)
    decoded_frame = cv2.imdecode(np_response_image, cv2.IMREAD_COLOR)
    ret, encoded_jpeg = cv2.imencode(DECODE_EXTENSION, decoded_frame)
    frame = encoded_jpeg.tobytes()
    # Return Decoded Image
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def frame_generator():
    while (True):
        # Decode Image
        decoded_frame = cv2.imdecode(np_response_image, cv2.IMREAD_COLOR)
        ret, encoded_jpeg = cv2.imencode(DECODE_EXTENSION, decoded_frame)
        frame = encoded_jpeg.tobytes()
        image = Image.frombytes("RGB", (1280, 720), np_response_image)
        imgByteArr = io.BytesIO()
        image.save(imgByteArr, format='JPEG')
        imgByteArr = imgByteArr.getvalue()
        frame = imgByteArr
        frame = np_response_image

        # Return Decoded Image
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# ROS node, publisher, and parameter.
# The node is started in a separate thread to avoid conflicts with Flask.
# The parameter *disable_signals* must be set if node is not initialized
# in the main thread.
threading.Thread(target = lambda:rospy.init_node('flask_node', disable_signals=True)).start()
push_pub = rospy.Publisher('/human_push', String, queue_size=1)
# NGROK = rospy.get_param('/ngrok', None) ??? WUT

subscriber = rospy.Subscriber("/camera/image/compressed",
    CompressedImage, callback,  queue_size = 1)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
    # app.run(host=os.environ['ROS_IP'], port=5000)
