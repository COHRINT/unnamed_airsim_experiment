#!/usr/bin/env python

import rospy

from geometry_msgs.msg import Twist

import sys, select, termios, tty
import airsim
import math

def drone_position():

    rospy.init_node('drone_position')
    # rate = rospy.Rate(10) # 10hz

    # Setup drone
    client = airsim.MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True, "Drone1")
    client.armDisarm(True)
    # Async methods returns Future. Call join() to wait for task to complete.
    client.takeoffAsync(vehicle_name="Drone1").join()
    # client.moveToPositionAsync(-10, 10, -10, 5).join()

    while not rospy.is_shutdown():
        x = input('x: ')
        y = input('y: ')
        z = input('altitude: ')
        speed = input('speed: ')
        print()
        client.moveToPositionAsync(x, y, -z, speed, vehicle_name="Drone1").join()


if __name__ == '__main__':
    try:
		drone_position()
    except rospy.ROSInterruptException:
        pass
