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
    pub = rospy.Publisher('/Drone1/cmd_vel', Twist, queue_size=10)
    r = rospy.Rate(4) # 4hz

    client = airsim.MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True, "Drone1")
    client.armDisarm(True)
    # # Async methods returns Future. Call join() to wait for task to complete.
    # client.takeoffAsync().join()

    msg = """
    Control The Drone!
    ---------------------------
    X/Y Plane Movement:
         i
    j    k    l

    Z Plane/Yaw:
         w
    a    s    d

    q/z : increase/decrease max speeds by 10%
    c/v : increase/decrease max yaw speed by 10%
    space key : stop
    """
    print(msg)

    speedBindings={
        'z':(1.1,1.1),
        'x':(.9,.9)
    }
    turnBindings={
        'c':(1.1,1.1),
        'v':(.9,.9)
    }

    speed = 2
    turn = 20

    while not rospy.is_shutdown():
        droneTwist = Twist()
        curState = client.getMultirotorState(vehicle_name="Drone1")
        newX = curX = curState.kinematics_estimated.position.x_val
        newY = curY = curState.kinematics_estimated.position.y_val
        newZ = curZ = curState.kinematics_estimated.position.z_val
        leftYaw = rightYaw = False
        # quaternion = (
        #     curState.kinematics_estimated.orientation.x_val,
        #     curState.kinematics_estimated.orientation.y_val,
        #     curState.kinematics_estimated.orientation.z_val,
        #     curState.kinematics_estimated.orientation.w_val)
        # curEuler = tf.transformations.euler_from_quaternion(quaternion)
        # newYaw = curYaw = curEuler[2]
        curYawRate = 0


        key = getKey()
        if key in speedBindings.keys():
            speed = speed * speedBindings[key][0]
            print(vels(speed,turn))
        elif key in turnBindings.keys():
            turn = turn * speedBindings[key][1]
            print(vels(speed,turn))
        elif key == 'i':
            newX += speed
            droneTwist.linear.x = speed
        elif key == 'k':
            newX -= speed
            droneTwist.linear.x = -speed
        elif key == 'j':
            newY -= speed
            droneTwist.linear.y = -speed
        elif key == 'l':
            newY += speed
            droneTwist.linear.y = speed
        elif key == 'w':
            newZ -= speed
            droneTwist.linear.z = -speed
        elif key == "s":
            newZ += speed
            droneTwist.linear.z = speed
        elif key == 'a':
            curYawRate = -turn
            droneTwist.angular.x = -turn
        elif key == "d":
            curYawRate = turn
            droneTwist.angular.x = turn

        client.enableApiControl(True, "Drone1")
        client.armDisarm(True, "Drone1")
        f1 = client.moveByVelocityAsync(newX-curX, newY-curY, newZ-curZ, .25,
                airsim.DrivetrainType.MaxDegreeOfFreedom,
                yaw_mode=airsim.YawMode(is_rate=True, yaw_or_rate=curYawRate),
                vehicle_name="Drone1")
        # f1.join()


        # z_vel = z * speed
        # yaw_rate = yaw * turn
        # pitch_rate = pitch * turn
        # roll_rate = roll * turn
        # twist.linear.x = pitch_rate; twist.linear.y = pitch_rate; twist.linear.z = z_vel
        # twist.angular.x = roll_rate; twist.angular.y = yaw_rate; twist.angular.z = pitch_rate
        pub.publish(droneTwist)

        # print("\n\n\n\n")
        # print(curState.kinematics_estimated.linear_acceleration.x_val)
        # print(curState.kinematics_estimated.linear_acceleration.y_val)
        # print(curState.kinematics_estimated.linear_acceleration.z_val)

        r.sleep()


if __name__ == '__main__':
    try:
        drone_teleop()
    except rospy.ROSInterruptException:
        pass
