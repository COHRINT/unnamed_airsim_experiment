#!/usr/bin/env python

import sys, select, termios, tty
import math
import signal
import airsim

import rospy
# from geometry_msgs.msg import Twist

import airsim_objects

def main():
    # setup ROS node
    rospy.init_node('airsim_bridge')

    # get airsim settings
    settings = airsim_objects.parseSettings("/home/tetsuo/Documents/AirSim/settings.json")

    # setup drone
    drone1 = airsim_objects.AirsimDrone("Drone1")

    # begin
    while not rospy.is_shutdown():
        drone1.publishImage()

    return 0


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
