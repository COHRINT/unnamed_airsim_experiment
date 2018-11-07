#!/usr/bin/env python

import rospy

from geometry_msgs.msg import Twist

import sys, select, termios, tty
import airsim
import math

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

    msg = """
    Control The Drone!
    ---------------------------
    Pitch/Roll:
         i
    j    k    l

    Throttle/Yaw:
         w
    a    s    d

    q/z : increase/decrease max speeds by 10%
    space key : stop
    """
    print(msg)

    speedBindings={
    'q':(1.1,1.1),
    'z':(.9,.9),
    'x':(.9,1),
    'e':(1,1.1),
    'c':(1,.9),
    }

    speed = 1
    turn = 1
    x = 0
    th = 0
    status = 0
    count = 0
    acc = 0.1

    z = 3
    yaw = 0

    while not rospy.is_shutdown():
        z = 0
        yaw = 0
        pitch = 0
        roll = 0


        key = getKey()
        # if key in moveBindings.keys():
        #     x = moveBindings[key][0]
        #     th = moveBindings[key][1]
        #     count = 0
        if key in speedBindings.keys():
            speed = speed * speedBindings[key][0]
            turn = turn * speedBindings[key][1]
            count = 0
            print(vels(speed,turn))
        elif key == 'i':
            pitch = 1
        elif key == 'k':
            pitch = 1
        elif key == 'j':
            roll = -1
        elif key == 'l':
            roll = 1
        elif key == 'w':
            z = -1
        elif key == "s":
            z = 1
        elif key == 'a':
            yaw = -10
        elif key == "d":
            yaw = 10
        elif key == ' ' or key == 'k' :
            # control_speed = 0
            # control_turn = 0
            print("Stopped")
        else:
            count = count + 1
            if count > 4:
                x = 0
                th = 0
            if (key == '\x03'):
                break

        z_vel = z * speed
        yaw_rate = yaw * turn
        pitch_rate = pitch * turn
        roll_rate = roll * turn
        # client.moveByAngleThrottleAsync(pitch=pitch_rate, roll=roll_rate, throttle=z_vel, yaw_rate=yaw_rate, duration=1, vehicle_name = 'Drone1')

        twist = Twist()
        twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
        pub.publish(twist)

def signal_handler(signal, frame):
	rospy.signal_shutdown("Stopping drone teleop")
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, termios.tcgetattr(sys.stdin))
	sys.exit(0)


if __name__ == '__main__':
    try:
        drone_teleop()
    except rospy.ROSInterruptException:
        pass
