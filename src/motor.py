#!/usr/bin/env python

import rospy
import message_filters
import cv2
from sensor_msgs.msg import Image
from std_msgs.msg import String
from std_msgs.msg import Float64
from std_msgs.msg import UInt16MultiArray
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge, CvBridgeError

def depth_sub:
    depth = message_filters.Subscriber("/camera/depth/image_rect_raw", Image)
    # pub1 = rospy.Publisher('test', UInt16MultiArray, queue_size=10)
    depth_image = self.bridge.imgmsg_to_cv2(depth_data, "32FC1")
    depth_array = np.array(depth_image, dtype=np.float32)
    cv2.imshow('test', depth_array)
    cv2.waitKey(3)

def callback(data):
    rospy.loginfo("get: %f", data.data)
    vel = UInt16MultiArray()
    vel.data = []
    pub = rospy.Publisher('cmd_vel', UInt16MultiArray, queue_size=10)
    if data.data <= 20:
        vel.data = [100,200]
        pub.publish(vel)
        
def gateway():
    rospy.init_node('Arduino', anonymous=True)
    rospy.Subscriber("chatter", Float64, callback)
    rospy.spin()

if __name__ == '__main__':
    gateway()
    
