#!/usr/bin/env python

# Example ROS node for publishing AirSim images.

# AirSim Python API
import setup_path
import airsim

import rospy
import numpy as np
import os

# ROS Image message
from sensor_msgs.msg import Image

def airpub():
    pub = rospy.Publisher("airsim/image_raw", Image, queue_size=1)
    rospy.init_node('image_raw', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    # connect to the AirSim simulator
    client = airsim.MultirotorClient()
    client.confirmConnection()

    while not rospy.is_shutdown():
        # # get camera images from drone
        # responses = client.simGetImages([
        #     # png format
        #     airsim.ImageRequest(0, airsim.AirSimImageType.Scene),
        #     # uncompressed RGBA array bytes
        #     airsim.ImageRequest(1, airsim.AirSimImageType.Scene, False, False),
        #     # floating point uncompressed image
        #     airsim.ImageRequest(1, airsim.AirSimImageType.DepthPlanner, True)])

        #  # get camera images from the car
        # responses = client.simGetImages([
        #     airsim.ImageRequest("1", airsim.ImageType.Scene, False, False)])  #scene vision image in uncompressed RGBA array

        responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])
        #         airsim.ImageRequest("0", airsim.ImageType.DepthVis),  #depth visualization image
        #         airsim.ImageType.Infrared
        response = responses[0]

        # get numpy array
        img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)

        # reshape array to 4 channel image array H X W X 4
        img_rgba = img1d.reshape(response.height, response.width, 4)

        # original image is fliped vertically
        img_rgba = np.flipud(img_rgba)

        # just for fun add little bit of green in all pixels
        # img_rgba[:,:,1:2] = 100

        filename = str(rospy.Time())

        # write to png
        airsim.write_png(os.path.normpath("images/drone/" + filename + '.png'), img_rgba)


        # for response in responses:
        #     img_rgba_string = response.image_data_uint8

        # Populate image message
        msg=Image()
        msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = "frameId"
        msg.encoding = "rgba8"
        msg.height = 720  # resolution should match values in settings.json
        msg.width = 1280
        # msg.data = img_rgba_string
        msg.is_bigendian = 0
        msg.step = msg.width * 4

        # log time and size of published image
        rospy.loginfo(msg)
        # publish image message
        pub.publish(msg)
        # # sleep until next cycle
        rate.sleep()


if __name__ == '__main__':
    try:
        airpub()
    except rospy.ROSInterruptException:
        pass
