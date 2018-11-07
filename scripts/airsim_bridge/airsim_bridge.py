#!/usr/bin/env python

import sys, select, termios, tty
import math
import signal

import rospy
from geometry_msgs.msg import Twist

import airsim_objects

droneTwist = Twist()
carTwist = Twist()

def main():
    # get airsim settings
    settings = airsim_objects.parseSettings("/home/tetsuo/Documents/AirSim/settings.json")
    settings["drone_name"] = "Drone1"

    # setup ROS node
    rospy.init_node('airsim_bridge')
    rospy.Subscriber("/%s/cmd_vel" % settings["drone_name"], Twist, droneTwistCallback)

    # setup vehicles
    drone = airsim_objects.AirsimDrone("Drone1")
    # car = airsim_objects.AirSimCar("Car1")
    drone.beginMovement().join()

    # begin
    while not rospy.is_shutdown():
        drone.publishImage()
        # f1 = drone.moveToPosition()
        # f2 = car.moveToPosition()
        # f1.join()
        # f2.join()

        rospy.sleep(1)

    return 0

def droneTwistCallback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
