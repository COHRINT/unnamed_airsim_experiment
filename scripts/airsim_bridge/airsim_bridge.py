#!/usr/bin/env python

# Use below in settings.json
"""
{
    ...
    "Vehicles": {
        "Drone1": {
          "VehicleType": "SimpleFlight",
          "X": 0, "Y": 0, "Z": -5,
          "Yaw": 90
        }
        "Car1": {
          "VehicleType": "PhysXCar",
          "X": 0, "Y": 0, "Z": -2
        }
    },
    "CommandMode": "Velocity" for velocity based movement, "Position" for position based movement
}

"""

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
    com_mode = settings["CommandMode"]
    drone_name = "Drone1" #settings["drone_name"] =
    car_name = "Car1" #settings["car_name"] =

    # setup ROS node
    rospy.init_node('airsim_bridge')
    # rospy.Subscriber("/%s/cmd_vel" % settings["drone_name"], Twist, droneTwistCallback)
    rospy.Subscriber("/%s/cmd_vel" % car_name, Twist, carTwistCallback)
    r = rospy.Rate(4) # 4hz

    # setup vehicles
    drone = airsim_objects.AirsimDrone(drone_name)
    drone.beginMovement().join()
    # droneTwist.linear.x = 0; droneTwist.linear.y = 0; droneTwist.linear.z = 0
    # droneTwist.angular.x = 0; droneTwist.angular.y = 0; droneTwist.angular.z = 0
    # car = airsim_objects.AirSimCar(settings["car_name"])
    # carTwist.linear.x = 0; carTwist.linear.y = 0; carTwist.linear.z = 0
    # carTwist.angular.x = 0; carTwist.angular.y = 0; carTwist.angular.z = 0

    # begin
    while not rospy.is_shutdown():
        # drone.publishImage()
        # car.publishImage()

        # f1 = drone.moveToPosition(droneTwist)
        # f2 = car.moveToPosition()
        f1 = drone.moveByVelocity(droneTwist)

        # f1.join()
        # f2.join()

        r.sleep()

    return 0

def droneTwistCallback(data):
    droneTwist = data.data

def carTwistCallback(data):
    carTwist = data.data


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
