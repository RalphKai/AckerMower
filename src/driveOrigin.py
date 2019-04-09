#!/usr/bin/env python
import getch
import roslib
import rospy

from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
from std_msgs.msg import Float32MultiArray

class drive():
	def __init__(self):
		self.rpm, self.left_ultra, self.right_ultra, self.forward_value = 0, 20, 20, 150
		self.forward_left_value, self.forward_right_value = 20, 20
		self.cmd_vel_publisher = rospy.Publisher("/cmd_vel", Twist, queue_size=10)			
		self.sensor_subscriber = rospy.Subscriber("/sensing", Float32MultiArray, self.call_back)
		# self.forward_subscriber = rospy.Subscriber("/forward_data", Float32MultiArray, self.call_back1)
		self.forward = 130.0
		self.angular = 26
		self.forward_init = 130.0
		self.angular_init = 26
		self.forward_forward = 146.0
		self.angular_left = 60.0
		self.angular_right = 0.0
		self.previous_status = [130.0, 26]
		self.init_state()
		self.unit_publish()
		self.rate = rospy.Rate(3)
		rospy.on_shutdown(self.shutdownhook)
		

	def init_state(self):
		rospy.loginfo(rospy.get_caller_id() + " init_state")
		twist = Twist()
		twist.linear.x = self.forward_init
		twist.angular.z = self.angular_init		
		self.cmd_vel_publisher.publish(twist)
	
	def forward_cmd(self):
		self.forward = self.forward_forward
		self.angular = self.angular_init
		

	def pause_cmd(self):
		self.forward = self.forward_init
	
	def backward_cmd(self):
		self.forward = 135
		self.unit_publish()
                rospy.sleep(0.65)
                self.forward = 110
                self.unit_publish()
		rospy.sleep(5)
		rospy.loginfo(rospy.get_caller_id() + " backward_inself")
		self.pause_cmd()
		

	def left_cmd(self):
		'''if self.forward == self.forward_forward:
			self.forward = self.forward_forward
			self.angular = self.angular_left
			self.unit_publish()'''
		if self.forward == 135 or self.forward == 110:
			pass
		else:
			self.forward = self.forward_forward + 1
			self.angular = self.angular_left
			self.unit_publish()
		# rospy.sleep(3)
		#self.angular = self.angular_init
		#self.unit_publish()

	def right_cmd(self):
		''''if self.forward == self.forward_forward:
			self.forward = self.forward_forward
			self.angular = self.angular_right
			self.unit_publish()'''
		if self.forward == 135 or self.forward == 110:
			pass
		else:
			self.forward = self.forward_forward + 1
			self.angular = self.angular_right
			self.unit_publish()
		# rospy.sleep(3)
		#self.angular = self.angular_init
		#self.unit_publish()
	# def right_total_free(self):
	def call_back(self, msg):
		self.left_ultra = msg.data[2]
		self.right_ultra = msg.data[1]
		self.rpm = msg.data[0]
		self.forward_value = msg.data[3]
		#self.forward_right_value = msg.data[4]
		#self.forward_left_value = msg.data[5]
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
		rospy.loginfo(rospy.get_caller_id() + " selfmove")
		#while(1):
		if (self.forward_value == 0.0 or (self.right_ultra == 0.0 and self.left_ultra == 0.0) ): # fix lossing msgs
			rospy.loginfo(rospy.get_caller_id() + " missing data but I fixed it")
			self.forward = self.previous_status[0]
			self.angular = self.previous_status[1]
			pass
		
		elif ( self.forward_value >= 100 and self.right_ultra > 40 and self.left_ultra > 40):
			self.forward_cmd()
	
		elif ( self.forward_value < 100 and self.right_ultra <= 40 and self.left_ultra <= 40):
			self.pause_cmd()
			self.backward_cmd()

		elif ( self.forward_value < 15 ):
			self.pause_cmd()
			self.backward_cmd()

		elif ( self.forward_value < 100 and self.left_ultra <= 40):
			self.right_cmd()

		elif ( self.forward_value < 100 and self.right_ultra <= 40):
			self.left_cmd()

		elif (self.forward_value < 100 and self.left_ultra > 40 and self.right_ultra > 40):
			self.left_cmd()

		self.previous_status = [self.forward, self.angular]
		
		'''if ( self.left_ultra >= 30 and self.right_ultra >=30 ):
			self.forward_cmd()
			rospy.loginfo(rospy.get_caller_id() + " forward_inself")

		else:
			self.pause_cmd()
			rospy.sleep(0.5)
			self.backward_cmd()
			rospy.loginfo(rospy.get_caller_id() + " backward_inself")'''
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
		rospy.sleep(1.0)   # 
	robot.shutdownhook(robot.shutdownhook)
	# robot.selfmove()
	rospy.spin()
