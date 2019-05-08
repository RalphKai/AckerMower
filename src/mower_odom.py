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

class Self_odom():
	def __init__(self):
		self.x = 0.6
		self.cmd_x = 0
		self.y = 0.6
		self.z = 0
		self.th = 0.
		self.vx = 0.
		self.vy = 0.
		self.vth = 0.
		self.yaw = 0
		self.rpm = 0
		self.tf_broadcaster = tf.TransformBroadcaster()
		self.odom_pub = rospy.Publisher("/odom_fake", Odometry, queue_size=10)
		self.cmd_subscriber = rospy.Subscriber("/cmd_vel", Twist, self.call_back_cmd)
		rospy.Rate(10)
		self.sensor_subscriber = rospy.Subscriber("/sensing", Float32, self.call_back)
		rospy.Rate(10)
		self.current_time = rospy.Time.now()
		self.last_time = rospy.Time.now()	
		rospy.on_shutdown(self.shutdownhook)
		
		
		
	def call_back(self, msg):
		# odometry data from hall sensors
		self.rpm = msg.data
		# self.rpm = (msg.data[0] * pi * 0.08) / 60
		

	def call_back_cmd(self, cmd):	
		self.cmd_x = cmd.linear.x
		if self.cmd_x <= 0.246 and self.cmd_x >0:
			self.cmd_x = 0.246
 	
		self.z = cmd.angular.z 
		rospy.loginfo("cmd_from_teb: "+ str(self.cmd_x) + ", "+ str(self.z))
		
		
	def tf_config(self):
		#rospy.loginfo("odomcallback_check:"+ str(self.rpm) + ", "+str(self.cmd_x))
		if self.cmd_x>0 and self.rpm>0:
			self.vx = self.cmd_x  # + 0.1 * ((self.rpm+11.603)/0.082)
			#rospy.loginfo("odomcallback vx: "+ str(self.vx))
		elif self.cmd_x<0 and self.rpm>0:
			self.vx = self.cmd_x 

		else:
			self.vx = 0

		if self.z>0:
			steering = self.convert_trans_rot_vel_to_steering_angle(self.cmd_x, self.z, 0.285)
			# self.vth = self.z
			self.vth = ( self.vx * tan(steering) / 0.285)
			# angular = 28 * (self.z/0.54)
			# self.vth = ( self.vx * tan(angular*(pi/180)) )/ 0.284
			# rospy.loginfo(rospy.get_caller_id() +" turn_angle: "+ str(steering)+", vz: "+ str(self.vth))
		elif self.z<0:
			steering = self.convert_trans_rot_vel_to_steering_angle(self.cmd_x, self.z, 0.285)
			#self.vth = self.z
			self.vth = ( self.vx * tan(steering)/ 0.285)
			# angular = -28 * (self.z/0.54)
			# self.vth = ( self.vx * tan(angular)*(pi/180) )/ 0.284
			
		else:
			self.vth = 0


	def convert_trans_rot_vel_to_steering_angle(self, v, omega, wheelbase):
  		if omega == 0 or v == 0:
    			return 0

  		radius = v / omega
		
  		return math.atan(wheelbase / radius)

	def pub_odom(self):
		self.tf_config()
		self.current_time = rospy.Time.now()
		dt = (self.current_time - self.last_time).to_sec()
		
		'''if(self.z!=0):
			delta_th = self.vth * dt
			self.th = self.th + delta_th'''

		delta_x = (self.vx * cos(self.th)) * dt   #  - self.vy * sin(self.th)
		delta_y = (self.vx * sin(self.th)) * dt   #  + self.vy * cos(self.th)

		
		delta_th = self.vth * dt
		

		self.th = self.th + delta_th
		yaw = self.th * (180/pi)

		self.x = self.x + delta_x
		self.y = self.y + delta_y

		self.last_time = self.current_time


		odom_quat = tf.transformations.quaternion_from_euler(0, 0, self.th)
		# publish odom
		odom = Odometry()
		odom.header.stamp = self.current_time
		odom.header.frame_id = "odom"

		odom.pose.pose = Pose(Point(self.x, self.y,0), Quaternion(*odom_quat))
		odom.child_frame_id = "base_link"
		
		
		odom.twist.twist = Twist(Vector3(self.vx, 0, 0), Vector3(0,0, self.vth))
		self.odom_pub.publish(odom)

		# publish tf
		
		rospy.loginfo("pub_tf: " + str(self.x) + ", "+ str(self.y) +", " +str(yaw))

		'''self.tf_broadcaster.sendTransform(
			(self.x, self.y, 0.0),
			odom_quat,
			self.current_time,
			"base_link",
			"odom"

		)
		'''

		
		# self.last_time = self.current_time

	def shutdownhook(self):
		rospy.loginfo(rospy.get_caller_id() + " stop")


if __name__ == '__main__':
	try:
		rospy.init_node('Mower_odom')
		self_odom = Self_odom()
		while not rospy.is_shutdown():
			self_odom.pub_odom()
	except rospy.ROSInterruptException:
    		pass
