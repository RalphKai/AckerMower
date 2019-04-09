#!/usr/bin/env python
import roslib
import rospy

from math import cos, sin, pi
import tf

from geometry_msgs.msg import Twist

class Converter():
	def __init__(self):
		self.cmd_x = 0
    		self.cmd_th = 0
    		self.pwm_x = 0
    		self.vy = 0
    		self.pwm_th = 0
	    	self.cmd_publisher = rospy.Publisher("/cmd_vel_toMotor", Twist, queue_size = 10)
	    	self.cmd_listener = rospy.Subscriber("/cmd_vel", Twist, self.callback)
	    	rospy.Rate(3)
	    	#rospy.spin()

	def forward_cmd(self):
		#global x
		#global vx
		self.pwm_x = (self.cmd_x + 11.603) / 0.082 # 140 + (self.x/0.37) * 6
		rospy.loginfo("pwm_x:"+str(self.pwm_x))

	def backward_cmd(self):
		rospy.loginfo("backward----------------------!!")
		#global vx
		self.pwm_x = 135
		self.pub_new_cmd()
		rospy.sleep(0.65)
		self.pwm_x = 110
		self.pub_new_cmd()
		rospy.sleep(1)

	def idle(self):
		# global vx
		self.pwm_x = 130	

	def processing(self):
		#global x
		#global th
		#global vth

		if self.cmd_x > 0:
			self.forward_cmd()
		elif self.cmd_x < 0:
			self.idle()
			self.backward_cmd()
		else:
			self.idle()

		if self.cmd_th > 0:
			self.pwm_th = 28 + (self.cmd_th/0.25) * 28
	  
		elif self.cmd_th < 0:
			self.pwm_th = 28 - (self.cmd_th/0.25) * 28
		
		else:
			self.pwm_th = 28

		self.pub_new_cmd()
		
	def callback(self, cmd):
		#global x
		#global th
		self.cmd_x = cmd.linear.x
		self.cmd_th = cmd.angular.z
	
		rospy.loginfo("callback_converter:"+str(self.cmd_x)+", " +str(self.cmd_th)+"----------------")
	def pub_new_cmd(self):
		#global vx
		#global vth
		#global cmd_publisher
		twist = Twist()
		twist.linear.x = self.pwm_x
		twist.angular.z = self.pwm_th
		self.cmd_publisher.publish(twist)
		rospy.loginfo("pub_in_converter:"+str(self.pwm_x)+", " +str(self.pwm_th))

	def shutdownhook(self):
		rospy.loginfo(rospy.get_caller_id() + " stop")

if __name__ == '__main__': 
  try:
    rospy.init_node('cmd_vel_to_ackermann_drive')
    converter = Converter()
    last_time = rospy.Time.now()
    current_time = rospy.Time.now()
    while not rospy.is_shutdown():
    	converter.processing()
    	rospy.loginfo("I'm in converter!!")
	rospy.sleep(0.1)
    # rospy.spin()
    
  except rospy.ROSInterruptException:
    pass



