#!/usr/bin/env python
import getch
import roslib
import rospy
import math
from math import cos, sin, pi
import tf

from geometry_msgs.msg import Twist, Point, Quaternion, Vector3, Pose
from std_msgs.msg import Float32
from std_msgs.msg import Float32MultiArray
from nav_msgs.msg import Odometry

class drive():
	def __init__(self):
		self.rpm, self.left_ultra, self.right_ultra, self.forward_value = 0, 20, 20, 150
		self.forward_left_value, self.forward_right_value = 20, 20
		self.cmd_vel_publisher = rospy.Publisher("/cmd_vel", Twist, queue_size=10)			
		self.sensor_subscriber = rospy.Subscriber("/sensing", Float32MultiArray, self.call_back)
		# self.forward_subscriber = rospy.Subscriber("/forward_data", Float32MultiArray, self.call_back1)
		self.odom_pub = rospy.Publisher("odom", Odometry, queue_size=10)
		self.odom_broadcaster = tf.TransformBroadcaster()
		# self.laser_broadcaster = tf.TransformBroadcaster()
		self.current_time = rospy.Time.now()
		self.last_time = rospy.Time.now()
		self.forward = 130.0
		self.angular = 26
		self.forward_init = 130.0
		self.angular_init = 26
		self.forward_forward = 146.0
		self.angular_left = 60.0
		self.angular_right = 0.0
		self.MAX_RANGE = 380
		self.speed = 0
		self.x = 0.
		self.y = 0.3
		self.th = 0.
		self.vx = 0.
		self.vy = 0.
		self.vth = 0.
		# for simulation / tf
		self.idle_sim = 0
		self.forward_sim = 0.3
		self.shift_sim = 0.15
		self.yaw_sim = 0.3
		self.init_state()
		self.unit_publish()
		self.rate = rospy.Rate(1)
		rospy.on_shutdown(self.shutdownhook)
		

	def init_state(self):
		rospy.loginfo(rospy.get_caller_id() + " init_state")
		twist = Twist()
		twist.linear.x = self.forward_init
		twist.angular.z = self.angular_init
		self.vx = self.idle_sim
		self.vy = self.idle_sim
		self.vth = self.idle_sim	
		self.cmd_vel_publisher.publish(twist)
	
	def forward_cmd(self):
		self.forward = self.forward_forward
		self.angular = self.angular_init
		self.vx = self.forward_sim
		rospy.loginfo(rospy.get_caller_id() + " +++forward+++")

	def pause_cmd(self):
		self.forward = self.forward_init
		self.vx = self.idle_sim
		self.vy = self.idle_sim
		rospy.loginfo(rospy.get_caller_id() + " ***pause***")
	
	def backward_cmd(self):
		self.forward = 135
		self.unit_publish()
                rospy.sleep(0.65)
                self.forward = 110
                self.unit_publish()
		rospy.sleep(1)
		if self.rpm != 0.0:
			rospy.sleep(4)
		rospy.loginfo(rospy.get_caller_id() + " ---backward---")
		self.pause_cmd()

	def left_cmd(self):
		rospy.loginfo(rospy.get_caller_id() + " ---left")
		if self.forward == 135 or self.forward == 110:
			pass
		elif self.forward_left_value < 35:
			pass
		else:
			self.forward = self.forward_forward + 1
			self.angular = self.angular_left
			self.vx = self.forward_sim
			self.vth = self.yaw_sim
			self.unit_publish()
		
		# rospy.sleep(3)
		#self.angular = self.angular_init
		#self.unit_publish()

	def right_cmd(self):
		''''if self.forward == self.forward_forward:
			self.forward = self.forward_forward
			self.angular = self.angular_right
			self.unit_publish()'''
		rospy.loginfo(rospy.get_caller_id() + " right---")
		if self.forward == 135 or self.forward == 110:
			pass
		elif self.forward_right_value < 35:
			pass
		else:
			self.forward = self.forward_forward + 1
			self.angular = self.angular_right
			self.vx = self.forward_sim
			self.vth = - self.yaw_sim
			self.unit_publish()
		
		# rospy.sleep(3)
		#self.angular = self.angular_init
		#self.unit_publish()
	# def right_total_free(self):
	def call_back(self, msg):
		if len(msg.data) == 6:
			self.left_ultra = msg.data[2]
			if self.left_ultra == 0:
				self.left_ultra = self.MAX_RANGE
			self.right_ultra = msg.data[1]
			if self.right_ultra == 0:
				self.right_ultra = self.MAX_RANGE
			self.rpm = msg.data[0]
			self.speed = self.rpm * ( (0.08*math.pi)/60 )
			self.forward_value = msg.data[3]
			if self.forward_value == 0:
				self.forward_value = self.MAX_RANGE
			self.forward_right_value = msg.data[4]
			if self.forward_right_value == 0:
				self.forward_right_value = self.MAX_RANGE
			self.forward_left_value = msg.data[5]
			if self.forward_left_value == 0:
				self.forward_left_value = self.MAX_RANGE
			rospy.loginfo([self.right_ultra, self.forward_right_value, self.forward_value, self.forward_left_value, self.left_ultra, self.rpm])
		else:
			pass
		#self.forward_value = msg.data[3]
		# rospy.loginfo(rospy.get_caller_id() + " call_back:" + str(self.left_ultra) + ", "+ str(self.right_ultra)
# + ", "+ str(self.forward_value)+ ", "+ str(self.forward_right_value)+ ", "+ str(self.forward_left_value))   
		
	
	def call_back1(self, msg):
		self.forward_value = msg.data[0]
		'''self.forward_left_value = msg.data[2]
		self.forward_right_value = msg.data[1]'''
		#self.forward_value = msg.data[3]
		#rospy.loginfo(rospy.get_caller_id() + " call_back1:" + str(self.forward_value))

	def selfmove(self):

		self.current_time = rospy.Time.now()
		
		dt = (self.current_time - self.last_time).to_sec()
		
		if (self.forward_value == 0.0 or (self.right_ultra == 0.0 and self.left_ultra == 0.0) ): # fix lossing msgs
			rospy.loginfo(rospy.get_caller_id() + " missing data but I fixed it")
			pass
		elif ( self.forward_value >= 110): # forward movement
			self.forward_cmd()

		elif ( self.forward_value < 10): # prevent crash
			self.pause_cmd()
			self.backward_cmd()
		elif ( self.forward_value >= 10 and self.forward_value <110):
			if self.forward_left_value < 10 or self.forward_right_value < 10: # prevent crash via bypass sensors
				self.pause_cmd()
				self.backward_cmd()

			elif self.right_ultra <= 65 and self.left_ultra <= 65: #  
				self.pause_cmd()				
				self.backward_cmd()

			elif self.forward_right_value <= 65:
				self.left_cmd()

			elif self.forward_left_value <= 65:
				self.right_cmd()
			
			else:
				self.left_cmd()
			
		'''elif ( self.forward_value < 100 and self.right_ultra <= 40 and self.left_ultra <= 40):
			self.backward_cmd()

		elif ( self.forward_value < 100 and self.left_ultra <= 40):
			self.right_cmd()

		elif ( self.forward_value < 100 and self.right_ultra <= 40):
			self.left_cmd()

		elif (self.forward_value < 100 and self.left_ultra > 40 and self.right_ultra > 40):
			self.left_cmd()'''

		
		'''if ( self.left_ultra >= 30 and self.right_ultra >=30 ):
			self.forward_cmd()
			rospy.loginfo(rospy.get_caller_id() + " forward_inself")

		else:
			self.pause_cmd()
			rospy.sleep(0.5)
			self.backward_cmd()
			rospy.loginfo(rospy.get_caller_id() + " backward_inself")'''
		delta_x = (self.vx * cos(self.th) - self.vy * sin(self.th)) * dt
		delta_y = (self.vx * sin(self.th) + self.vy * cos(self.th)) * dt
		delta_th = self.vth * dt
		rospy.loginfo("delta_x, y, th:" + str(delta_x) + str(delta_y) + str(delta_th))
		self.x = self.x + delta_x
		self.y = self.y + delta_y
		self.th = self.th + delta_th
		rospy.loginfo("self_x, y, th:" + str(self.x) + str(self.y) + str(self.th))
		odom_quat = tf.transformations.quaternion_from_euler(0, 0, self.th)
		
		self.odom_broadcaster.sendTransform(
			(self.x, self.y, 0),
			odom_quat,
			self.current_time,
			"base_link",
			"odom"

		)
		
		'''self.laser_broadcaster.sendTransform(
			(0, 0, 0),
			(0, 0, 0, 1),
			self.current_time,
			"scan",
			"base_link"
		)'''
		odom = Odometry()
		odom.header.stamp = self.current_time
		odom.header.frame_id = "odom"

		odom.pose.pose = Pose(Point(self.x, self.y,0), Quaternion(*odom_quat))
		
		odom.child_frame_id = "base_link"
		odom.twist.twist = Twist(Vector3(self.vx, self.vy, 0), Vector3(0,0, self.vth))

		self.odom_pub.publish(odom)

		self.last_time = self.current_time
		self.unit_publish()

	def shutdownhook(self):
		rospy.loginfo(rospy.get_caller_id() + " stop")
		twist = Twist()
		twist.linear.x = self.forward_init
		twist.angular.z = self.angular_init
		self.cmd_vel_publisher.publish(twist)
		rospy.loginfo(rospy.get_caller_id() + "shutdown")

	def unit_publish(self):
		twist = Twist()
		twist.linear.x = self.forward
		twist.angular.z = self.angular
		rospy.loginfo(rospy.get_caller_id() + "publish:" + str(twist.linear.x) + ", "+ str(twist.angular.z))
		self.cmd_vel_publisher.publish(twist)

if __name__ == '__main__':
	rospy.init_node('userToMower')
	robot = drive()
	while not rospy.is_shutdown():
		robot.selfmove()
		rospy.sleep(1)   # 
	rospy.on_shutdown(robot.shutdownhook)
	# robot.selfmove()
	rospy.spin()
