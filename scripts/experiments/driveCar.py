#!/usr/bin/env python

import rospy

import sys, select, termios, tty
import airsim
import math
import time

def drive_car():

    rospy.init_node('drive_car')
    # rate = rospy.Rate(10) # 10hz

    # Setup drone
    client = airsim.CarClient()
    client.confirmConnection()
    client.enableApiControl(True, "Car1")
    client.armDisarm(True)
    # Async methods returns Future. Call join() to wait for task to complete.
    client.takeoffAsync().join()
    # client.moveToPositionAsync(-10, 10, -10, 5).join()

    # # List of goals
    # goals = [{"throttle: "}
    #     car_controls1.throttle = 0.5
    #     car_controls1.steering = 0.5
    #
    #     print("Car1: Go Forward")
    # ]

    forward = airsim.CarControls()
    forward.throttle = 0.5
    forward.steering = 0.5
    brake = airsim.CarControls()
    brake.brake = 1
    turn90 = airsim.CarControls()
    turn90.throttle = 0.5
    turn90.steering = 0

    print("Initating square movement of car")

    while not rospy.is_shutdown():
        print("Forward")
        client.setCarControls(forward, "Car1")
        time.sleep(4)   # let car drive a bit

        print("Braking")
        client.setCarControls(brake, "Car1")
        time.sleep(1)

        print("Turning")
        client.setCarControls(turn90, "Car1") # turn 90 degrees
        time.sleep(1)
        # client.moveToPositionAsync(x, y, -z, speed, vehicle_name="Drone1").join()



if __name__ == '__main__':
    try:
		drive_car()
    except rospy.ROSInterruptException:
        pass
