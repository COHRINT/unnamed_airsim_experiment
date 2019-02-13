#!/usr/bin/env python

import sys, select, termios, tty
import math
import signal
import json
# sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
# import cv2
import numpy as np
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
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
        self.image_pub = rospy.Publisher("/%s/output/image_raw/compressed" % self.name, CompressedImage)

    def beginMovement(self):
        self.client.enableApiControl(True, self.name)
        self.client.armDisarm(True, self.name)
        return self.client.takeoffAsync(vehicle_name=self.name)

    def publishImage(self, type="color"):
        response_image = self.client.simGetImage(CAMERA_NAME, IMAGE_TYPE)
        np_response_image = np.asarray(bytearray(response_image), dtype="uint8")
        # Publish to ROS
        msg = CompressedImage()
        msg.header.stamp = rospy.Time.now()
        msg.format = "jpeg"
        msg.data = np_response_image.tostring()
        # msg.data = np.array(cv2.imencode('.jpg', image_np)[1]).tostring()
        self.image_pub.publish(msg)


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
    def moveToPosition(self, pos_msg, cur_pos=False):
        self.client.enableApiControl(True, self.name)
        self.client.armDisarm(True, self.name)
        vx, vy, vz = droneTwist.linear.x, droneTwist.linear.y, droneTwist.linear.z
        speed = 1 # vel.x + vel.y + vel.z^2 blah
        if (cur_pos):
            return self.client.moveToPositionAsync(0, 0, 0, speed, vehicle_name=self.name)
        else:
            return self.client.moveByVelocityAsync(vx, vy, vz, 1, self.name)

    def moveByVelocity(self, pos_msg):
        self.client.enableApiControl(True, self.name)
        self.client.armDisarm(True, self.name)
        f1 = self.client.moveByVelocityAsync(pos_msg.linear.x, pos_msg.linear.y, pos_msg.linear.z, .25,
                airsim.DrivetrainType.MaxDegreeOfFreedom,
                yaw_mode=airsim.YawMode(is_rate=True, yaw_or_rate=pos_msg.angular.x),
                vehicle_name=self.name)

class AirSimCar():
    def __init__(self, name="Car1"):
        self.client = airsim.CarClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True, name)
        self.client.armDisarm(True)

        self.name = name
        self.image_pub = rospy.Publisher("/%s/output/image_raw/compressed" % self.name, CompressedImage)

    def moveToPosition(self, pos_msg=""):
        self.client.enableApiControl(True, name)
        self.client.armDisarm(True, name)
        speed = 1 # vel.x + vel.y + vel.z^2 blah
        return self.client.moveToPositionAsync(0, 0, 0, speed, vehicle_name=name)

    def publishImage(self, type="color"):
        response_image = self.client.simGetImage(CAMERA_NAME, IMAGE_TYPE)
        np_response_image = np.asarray(bytearray(response_image), dtype="uint8")
        # Publish to ROS
        msg = CompressedImage()
        msg.header.stamp = rospy.Time.now()
        msg.format = "jpeg"
        msg.data = np_response_image.tostring()
        # msg.data = np.array(cv2.imencode('.jpg', image_np)[1]).tostring()
        self.image_pub.publish(msg)

def parseSettings(json_loc):
    with open(json_loc) as json_file:
        data = json.load(json_file)
        return data
    return None
