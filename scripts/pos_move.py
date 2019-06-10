#!/usr/bin/env python

'''
CHANGE settings.json TO "SimMode": "Multirotor"


,"Car1": {
  "VehicleType": "PhysXCar",
  "X": 8, "Y": 0, "Z": -2,
"Yaw": 180
}

"Drone1": {
"VehicleType": "SimpleFlight",
"DefaultVehicleState": "Inactive",
"RC": {
"RemoteControlID": 0
},
"X": 4, "Y": 0, "Z": -2
}

'''

import rospy

# from geometry_msgs.msg import Twist, PoseStamped, Point, Quaternion
import geometry_msgs.msg as geo_msgs
import std_msgs.msg as std_msgs

import sys, select, termios, tty
# import airsim
import math
import tf

import signal


def pos_move():

    rospy.init_node('position_movement_test')
    pub = rospy.Publisher('/Drone1/pose', geo_msgs.PoseStamped, queue_size=10)
    r = rospy.Rate(4) # 4hz

    # client = airsim.MultirotorClient()
    # client.confirmConnection()
    # client.enableApiControl(True, "Drone1")
    # client.armDisarm(True)
    # # Async methods returns Future. Call join() to wait for task to complete.
    # client.takeoffAsync().join()
    # x = 10
    # y = 10
    # z = 15
    #
    # print("goin")
    # f1 = client.moveToPositionAsync(x, y, -1*z, 1, timeout_sec=25,
    #             drivetrain=airsim.DrivetrainType.MaxDegreeOfFreedom,
    #             yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=0),
    #             vehicle_name="Drone1")
    #
    # f1.join()
    # print("showed")

    while not rospy.is_shutdown():
        x = raw_input("x: ")
        y = raw_input("y: ")
        z = raw_input("z: ")
        pt = geo_msgs.Point(float(x), float(y), -1*float(z))
        qt = geo_msgs.Quaternion(0, 0, 0, 0) # xyzw
        print("sending pose: (%d, %d, %d", x, y, z)
        nextPose = geo_msgs.PoseStamped(std_msgs.Header(), geo_msgs.Pose(pt, qt))
        pub.publish(nextPose)
        print("Published")
        r.sleep()


if __name__ == '__main__':
    try:
        pos_move()
    except rospy.ROSInterruptException:
        pass
