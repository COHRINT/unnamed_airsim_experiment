#!/usr/bin/env python
import cv2
import cv_bridge
import rospy
import geometry_msgs.msg as geo_msgs
import airsim_bridge
from airsim_bridge.srv import *
import threading

import unrealcv
def main():
    # set_location_service = rospy.ServiceProxy('set_camera_location', SetCameraLocation)
    # set_rotation_service = rospy.ServiceProxy('set_camera_rotation', SetCameraRotation)
    # get_image_service = rospy.ServiceProxy('get_camera_view', GetCameraImage)
    #
    # # set_location_service(0, geo_msgs.Point(x=100, y=-270, z=100))
    # # set_rotation_service(0, geo_msgs.Quaternion(w=0.70710678, x=0, y=0, z=-0.70710678))
    # # response = get_image_service(0, 'depth')
    #
    # response = get_image_service(0, 'depth')
    #
    # opencv_bridge = cv_bridge.CvBridge()
    # image = opencv_bridge.imgmsg_to_cv2(response.image)
    # cv2.imshow('test', image)
    # cv2.waitKey()


    # host = unrealcv.HOST
    #port = unrealcv.PORT

    # from unrealcv import client

    opencv_bridge = cv_bridge.CvBridge()

    # _client_lock = threading.Lock()
    # client = unrealcv.Client(endpoint=(host, port))
    client = unrealcv.Client(('127.0.0.1', 9234))# '127.0.0.1' is the server IP address, 9001 is the server port ID, please change it to align to your UnrealCV server.

    # import unrealcv
    # client = unrealcv.Client(('127.0.0.1', 9001))# '127.0.0.1' is the server IP address, 9001 is the server port ID, please change it to align to your UnrealCV server.
    client.connect()
    # if not client.isconnected(): # Check if the connection is successfully established
    #   print('UnrealCV server is not running. Run the game from http://unrealcv.github.io first.')
    # else:
    # print("Hello")
    res = client.request('vget /unrealcv/status')
    print(res)
    print("end")
    filename = client.request('vget /camera/0/lit')
    print(filename)

    filename = client.request('vget /camera/0/depth depth.exr')
    print(filename)

    loc = client.request('vget /camera/0/location')
    print(loc)

    client.request('vset /camera/1/location [6600] [5600] [743]')
    filename = client.request('vget /camera/1/lit')
    print(filename)

    # It is also possible to get the png directly without saving to a file
    # res = client.request('vget /camera/0/lit png')
    # im = read_png(res)
    # print(im.shape)


if __name__ == "__main__":
    main()
