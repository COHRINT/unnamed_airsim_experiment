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
    # rate = rospy.Rate(10) # 10hz
    signal.signal(signal.SIGINT, signal_handler)

    # Setup drone
    client = airsim.MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True, "Drone1")
    client.armDisarm(True)
    # Async methods returns Future. Call join() to wait for task to complete.
    # client.takeoffAsync().join()
    # client.moveToPositionAsync(-10, 10, -10, 5).join()

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

	# client.takeoffAsync().join()
    # f1 = client.takeoffAsync(vehicle_name="Drone1")
    # f2 = client.takeoffAsync(vehicle_name="Drone2")
    start_x = 0
    start_y = 0
    f1 = client.moveToPositionAsync(start_x, start_y, -3,  3, vehicle_name="Drone1")
    # f2 = client.moveToPositionAsync(-8, start_y, -3,  3, vehicle_name="Drone2")
    f1.join()
    # f2.join()


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

        # target_turn = turn * th

        # if target_speed > control_speed:
        #     control_speed = min( target_speed, control_speed + 0.02 )
        # elif target_speed < control_speed:
        #     control_speed = max( target_speed, control_speed - 0.02 )
        # else:
        #     control_speed = target_speed
        #
        # if target_turn > control_turn:
        #     control_turn = min( target_turn, control_turn + 0.1 )
        # elif target_turn < control_turn:
        #     control_turn = max( target_turn, control_turn - 0.1 )
        # else:
        #     control_turn = target_turn

        # x_vel = speed * math.cos(target_turn)
        # y_vel = speed * math.sin(target_turn)

        z_vel = z * speed
        yaw_rate = yaw * turn
        pitch_rate = pitch * turn
        roll_rate = roll * turn
        client.moveByAngleThrottleAsync(pitch=pitch_rate, roll=roll_rate, throttle=z_vel, yaw_rate=yaw_rate, duration=1, vehicle_name = 'Drone1')
        # yaw_mode = airsim.YawMode(is_rate= True, yaw_or_rate = 0)
        # client.moveToZAsync(-z, speed, vehicle_name="Drone1")
        # client.moveByVelocityZAsync(x_vel, y_vel, -3, 1, vehicle_name="Drone1")
        # client.moveByVelocityZAsync(x_vel, y_vel, -3, 1, vehicle_name="Drone1")
        # client.rotateByYawRateAsync(yaw_rate, 1, vehicle_name="Drone1")

        # twist = Twist()
        # twist.linear.x = control_speed; twist.linear.y = 0; twist.linear.z = 0
        # twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = control_turn
        # pub.publish(twist)
        # client.moveByRC(rcdata = airsim.RCData(pitch = 0.0, throttle = 1.0, is_initialized = True, is_valid = True))
        # rospy.loginfo(key)
        # speed_x = control_speed
        # pitch, roll, yaw  = client.getPitchRollYaw()
        # vel = self.getVelocity()
        # vx = math.cos(yaw) * speed_x - math.sin(yaw) * speed_y
        # vy = math.sin(yaw) * speed_x + math.cos(yaw) * speed_y
        # if speed_x <= 0.01:
        # elif speed_x > 0.01:
        #     drivetrain = DrivetrainType.ForwardOnly
        #     yaw_mode = YawMode(is_rate= False, yaw_or_rate = 0)
        # moveByVelocityZAsync(vx = (vx +vel.x_val)/2 ,
        #                      vy = (vy +vel.y_val)/2 , #do this to try and smooth the movement
        #                      z = self.z,
        #                      duration = .05 + 5,
        #                      drivetrain = drivetrain,
        #                      yaw_mode = yaw_mode)

def signal_handler(signal, frame):
	rospy.signal_shutdown("Stopping drone teleop")
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, termios.tcgetattr(sys.stdin))
	sys.exit(0)


if __name__ == '__main__':
    try:
        drone_teleop()
    except rospy.ROSInterruptException:
        pass
