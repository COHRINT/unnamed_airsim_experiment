#!/usr/bin/env python

import rospy

import sys, select, termios, tty
import airsim
import math

def drone_teleop():

    rospy.init_node('square')
    # rate = rospy.Rate(10) # 10hz

    # Setup drone
    client = airsim.MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True, "Drone1")
    client.enableApiControl(True, "Drone2")
    client.armDisarm(True, "Drone1")
    client.armDisarm(True, "Drone2")

    airsim.wait_key('Press any key to takeoff')
    f1 = client.takeoffAsync(vehicle_name="Drone1")
    f2 = client.takeoffAsync(vehicle_name="Drone2")
    f1.join()
    f2.join()

    # List of goals
    goals1 = [{"x": -1, "y": 1, "z": -5},
        {"x": 1, "y": 1, "z": -5},
        {"x": 1, "y": -1, "z": -5},
        {"x": -1, "y": -1, "z": -5}
    ]
    goals2 = [{"x": 1, "y": 1, "z": -5},
        {"x": 1, "y": -1, "z": -5},
        {"x": -1, "y": -1, "z": -5},
        {"x": -1, "y": 1, "z": -5}
    ]

    speed = 10

    i = 0
    while not rospy.is_shutdown():
        airsim.wait_key('Next Goal')
        print("x:" + str(goals1[i]["x"]))
        print("y: " + str(goals1[i]["y"]))
        print("z: " + str(goals1[i]["z"]))
        client.enableApiControl(True, "Drone1")
        client.enableApiControl(True, "Drone2")
        client.armDisarm(True, "Drone1")
        client.armDisarm(True, "Drone2")
        f1 = client.moveToPositionAsync(goals1[i]["x"], goals1[i]["y"], goals1[i]["z"], speed, vehicle_name="Drone1")
        f2 = client.moveToPositionAsync(goals2[i]["x"], goals2[i]["y"], goals2[i]["z"], speed, vehicle_name="Drone2")
        f1.join()
        f2.join()
        print("Goal Reached!")
        i += 1
        if (i >= len(goals1)):
            i = 0

    client.armDisarm(False, "Drone1")
    client.armDisarm(False, "Drone2")
    client.reset()

    # that's enough fun for now. let's quit cleanly
    client.enableApiControl(False, "Drone1")
    client.enableApiControl(False, "Drone2")


if __name__ == '__main__':
    try:
        drone_teleop()
    except rospy.ROSInterruptException:
        pass
