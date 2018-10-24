#!/usr/bin/env python

import rospy

import sys, select, termios, tty
import airsim
import math
import time

def waypoint_drone():

    rospy.init_node('waypoint_drone')
    # rate = rospy.Rate(10) # 10hz

    # Setup drone
    client = airsim.MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True, "Drone2")
    client.armDisarm(True)

    print("Initating waypoint following")

    # Async methods returns Future. Call join() to wait for task to complete.\
    client.takeoffAsync(vehicle_name="Drone2").join()
    # client.moveToPositionAsync(-10, 10, -10, 5).join()

    # List of goals
    goals = [{"x": -1, "y": 1, "z": -5},
        {"x": 1, "y": 1, "z": -5},
        {"x": 1, "y": -1, "z": -5},
        {"x": -1, "y": -1, "z": -5}
    ]

    speed = 50

    i = 0
    while not rospy.is_shutdown():
        print("x:" + str(goals[i]["x"]))
        print("y: " + str(goals[i]["y"]))
        print("z: " + str(goals[i]["z"]))
        if (i >= len(goals)):
            i = 0
        client.moveToPositionAsync(goals[i]["x"], goals[i]["y"], goals[i]["z"], speed, vehicle_name="Drone2").join()
        print("Goal Reached!")
        i += 1



if __name__ == '__main__':
    try:
		waypoint_drone()
    except rospy.ROSInterruptException:
        pass
