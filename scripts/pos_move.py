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

from geometry_msgs.msg import Twist

import sys, select, termios, tty
import airsim
import math
import tf

import signal

def getKey():
   tty.setraw(sys.stdin.fileno())
   rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
   if rlist:
       key = sys.stdin.read(1)
   else:
       key = ''

   termios.tcsetattr(sys.stdin, termios.TCSADRAIN, termios.tcgetattr(sys.stdin))
   return key


def vels(speed,turn):
   return "currently:\tspeed %s\tturn %s " % (speed,turn)

def drone_teleop():

    rospy.init_node('drone_teleop')
    pub = rospy.Publisher('/Drone1/', Twist, queue_size=10)
    r = rospy.Rate(4) # 4hz

    client = airsim.MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True, "Drone1")
    client.armDisarm(True)
    # # Async methods returns Future. Call join() to wait for task to complete.
    # client.takeoffAsync().join()


    while not rospy.is_shutdown():
        droneTwist = Twist()
        curState = client.getMultirotorState(vehicle_name="Drone1")



        # client.enableApiControl(True, "Drone1")
        # client.armDisarm(True, "Drone1")
        # f1 = client.moveByVelocityAsync(newX-curX, newY-curY, newZ-curZ, .25,
        #         airsim.DrivetrainType.MaxDegreeOfFreedom,
        #         yaw_mode=airsim.YawMode(is_rate=True, yaw_or_rate=curYawRate),
        #         vehicle_name="Drone1")

        pub.publish(droneTwist)


        r.sleep()


if __name__ == '__main__':
    try:
        pos_move()
    except rospy.ROSInterruptException:
        pass
