#!/usr/bin/env python

import roslib
import rospy
import math
from math import cos, sin, pi, tan, atan
import tf

from geometry_msgs.msg import Twist, Point, Quaternion, Vector3, Pose
from std_msgs.msg import Float32
from std_msgs.msg import Float32MultiArray
from nav_msgs.msg import Odometry

class hall_convert():
	def __init__(self):
		self.rpm = 0
		self.speed = 0
		self.cmd_x = 0
		self.odom_pub = rospy.Publisher("/odom_hall", Odometry, queue_size=10)
		self.sensor_subscriber = rospy.Subscriber("/sensing", Float32, self.call_back)
		rospy.Rate(30)
		self.cmd_subscriber = rospy.Subscriber("/cmd_vel", Twist, self.call_back_cmd)
		rospy.Rate(30)
		rospy.on_shutdown(self.shutdownhook)

	def call_back_cmd(self, cmd):	
		self.cmd_x = cmd.linear.x 	
		
		
	def call_back(self, msg):
		# odometry data from hall sensors
		self.rpm = msg.data
		if self.rpm !=0:
			self.speed = 0.0549 + 0.0043 * self.rpm
		else:
			self.speed = 0
		if self.cmd_x <0:
			self.speed = -self.speed
		# rospy.loginfo("self.speed: "+str(self.speed))
		# self.rpm = (msg.data[0] * pi * 0.08) / 60
		

	def pub_odom(self):
		odom_quat = tf.transformations.quaternion_from_euler(0, 0, 0)
		# publish odom
		odom = Odometry()
		odom.header.stamp = rospy.Time.now()
		odom.header.frame_id = "odom"
		odom.pose.pose = Pose(Point(0, 0,0), Quaternion(*odom_quat))
		odom.child_frame_id = "base_link"
		odom.twist.twist = Twist(Vector3(self.speed, 0, 0), Vector3(0,0, 0))
		self.odom_pub.publish(odom)



	def shutdownhook(self):
		rospy.loginfo(rospy.get_caller_id() + " stop")


if __name__ == '__main__':
	try:
		rospy.init_node('hall_converter')
		hall = hall_convert()
		while not rospy.is_shutdown():
			hall.pub_odom()
	except rospy.ROSInterruptException:
    		pass
