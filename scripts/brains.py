#!/usr/bin/env python

# Dependencies
import sys, select, termios, tty
import math
import tf
import signal
# ROS Dependencies
import rospy
import geometry_msgs.msg as geo_msgs
import std_msgs.msg as std_msgs

class POMDP:
    def __init__(self):
        rospy.init_node('position_movement_test')
        posMovePub = rospy.Publisher('/Drone1/pose', geo_msgs.PoseStamped, queue_size=10)
        r = rospy.Rate(4) # 4hz

        # pt = geo_msgs.Point(float(x), float(y), -1*float(z))
        # qt = geo_msgs.Quaternion(0, 0, 0, 0) # xyzw
        # nextPose = geo_msgs.PoseStamped(std_msgs.Header(), geo_msgs.Pose(pt, qt))
        # pub.publish(nextPose)

        r.sleep()


if __name__ == '__main__':
    try:
        POMDP()
    except rospy.ROSInterruptException:
        pass
