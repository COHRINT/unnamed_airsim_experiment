#!/usr/bin/env python

import rospy

import sys, select, termios, tty
import airsim
import math
import random
"""
In settings.json:
    "Drone2": {
      "VehicleType": "SimpleFlight",
      "DefaultVehicleState": "Inactive",
       "X": 8, "Y": 0, "Z": -2
    }
"""

def drone_chase():

    rospy.init_node('chase')
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

    x1 = -1 * random.randint(2, 7)
    y1 = random.randint(-3, 4)
    z1 = random.randint(-7, -4)
    x2 = -1 * random.randint(2, 6)
    y2 = random.randint(2, 5)
    z2 = random.randint(-7, -4)
    speed1 = random.randint(1, 3)
    speed2 = speed1 + 1
    f1 = client.moveToPositionAsync(x1, y1, z1, speed1, vehicle_name="Drone1")
    f2 = client.moveToPositionAsync(x2, y2, z2, speed2, vehicle_name="Drone2")
    f1.join()
    f2.join()
    print("x:" + str(x1))
    print("y: " + str(y1))
    print("z: " + str(z1))

    # f1 = client.rotateToYawAsync(180., vehicle_name ="Drone1")
    # f2 = client.rotateToYawAsync(180., vehicle_name ="Drone2")
    # f1.join()
    # f2.join()
    # print("turned")

    while not rospy.is_shutdown():
        x1 = x1 + -1 * random.randint(2, 4)
        y1 = random.randint(y1-3, y1+4)
        z1 = random.randint(z1-1, z1+1)
        x2 = x1 + random.randint(2, 4)
        y2 = random.randint(y1+2, y1+5)
        z2 = random.randint(z1-1, z1+1)
        speed1 = random.randint(1, 3)
        speed2 = speed1 + 1

        client.enableApiControl(True, "Drone1")
        client.enableApiControl(True, "Drone2")
        client.armDisarm(True, "Drone1")
        client.armDisarm(True, "Drone2")
        f1 = client.moveToPositionAsync(x1, y1, z1, speed1, vehicle_name="Drone1",
            drivetrain=airsim.DrivetrainType.MaxDegreeOfFreedom,
            yaw_mode=airsim.YawMode(is_rate=True, yaw_or_rate=20))
        f2 = client.moveToPositionAsync(x2, y2, z2, speed2, vehicle_name="Drone2")
        # f1.join()
        # f2.join()

        print("\n\n\n\nx:" + str(x1))
        print("y: " + str(y1))
        print("z: " + str(z1))
        print("\n\nDrone1:")
        print(client.getMultirotorState(vehicle_name="Drone1"))
        print("\n\nDrone2:")
        print(client.getMultirotorState(vehicle_name="Drone2"))

        rospy.sleep(2)

    client.armDisarm(False, "Drone1")
    client.armDisarm(False, "Drone2")
    client.reset()

    # that's enough fun for now. let's quit cleanly
    client.enableApiControl(False, "Drone1")
    client.enableApiControl(False, "Drone2")


if __name__ == '__main__':
    try:
        drone_chase()
    except rospy.ROSInterruptException:
        pass
