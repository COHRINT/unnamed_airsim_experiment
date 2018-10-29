#!/usr/bin/env python

import sys, select, termios, tty
import math
import signal
# sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import numpy as np
import airsim

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import CompressedImage

CAMERA_NAME = '0'
IMAGE_TYPE = airsim.ImageType.Scene
DECODE_EXTENSION = '.jpg'



class AirsimDrone():
    def __init__(self, name):
        # Setup Drone API Control in AirSim
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True, name)
        self.client.armDisarm(True, name)

        self.name = name
        image_pub = rospy.Publisher("/%s/output/image_raw/compressed" % self.name, CompressedImage)

    def publishImage(self, type="color"):
        response_image = self.client.simGetImage(CAMERA_NAME, IMAGE_TYPE)
        np_response_image = np.asarray(bytearray(response_image), dtype="uint8")
        # Publish to ROS
        msg = CompressedImage()
        msg.header.stamp = rospy.Time.now()
        msg.format = "jpeg"
        msg.data = np_response_image.tostring()
        # msg.data = np.array(cv2.imencode('.jpg', image_np)[1]).tostring()
        image_pub.publish(msg)


    # def generateVideoStream(self):
    #     while (True):
    #         # Get Image
    #         response_image = client.simGetImage(CAMERA_NAME, IMAGE_TYPE)
    #         np_response_image = np.asarray(bytearray(response_image), dtype="uint8")
    #         # Publish to ROS
    #
    #          msg = CompressedImage()
    #          msg.header.stamp = rospy.Time.now()
    #          msg.format = "jpeg"
    #          msg.data = np_response_image.tostring()
    #          # msg.data = np.array(cv2.imencode('.jpg', image_np)[1]).tostring()
    #          image_pub.publish(msg)
    #
    #         # Return Image
    #         # yield (b'--frame\r\n'
    #         #        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    #
    # def moveToPosition(self, pos_msg):
    #     return 0

class AirSimCar():
    def __init__(self):
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True, "Drone1")
        self.client.enableApiControl(True, "Drone2")
        self.client.armDisarm(True)

def parseSettings(json_loc):
    return {}
