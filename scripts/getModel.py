#!/usr/bin/env python

import rospy

# from geometry_msgs.msg import Twist, PoseStamped, Point, Quaternion
import geometry_msgs.msg as geo_msgs
import std_msgs.msg as std_msgsPlaye

import sys, select, termios, tty
import airsim
import math
import tf

import signal


def getModel():

    client = airsim.MultirotorClient()
    client.confirmConnection()

    while True:
        x = raw_input("Enter Model Name: ")
        print(x)
        p = client.simGetObjectPose(x);
        print(p)


if __name__ == '__main__':
    try:
        getModel()
    except rospy.ROSInterruptException:
        pass
