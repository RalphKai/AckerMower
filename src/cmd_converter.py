#!/usr/bin/env python
import roslib
import rospy

from math import cos, sin, pi, atan
import tf

from geometry_msgs.msg import Twist
from std_msgs.msg import Float32

class Converter():
	def __init__(self):
		self.cmd_x = 0
    		self.cmd_vth = 0
		self.conv_th = 0
    		self.pwm_x = 0
    		self.vy = 0
    		self.pwm_th = 0
		self.rpm = 0
		self.last_time = rospy.Time.now()
		self.current = self.last_time
	    	self.cmd_publisher = rospy.Publisher("/cmd_vel_toMotor", Twist, queue_size = 3)
	    	self.cmd_listener = rospy.Subscriber("/cmd_vel", Twist, self.callback)
		rospy.Rate(5)
		self.sensor_subscriber = rospy.Subscriber("/sensing", Float32, self.call_back_sensor)
	    	rospy.Rate(5)
	    	#rospy.spin()

	def forward_cmd(self):
		#global x
		#global vx
		self.pwm_x = (self.cmd_x + 11.603) / 0.082 #0.082 # 140 + (self.x/0.37) * 6
		if self.pwm_x > 140 and self.pwm_x < 144.5:
			self.pwm_x = 144.5
		self.pub_new_cmd()
		# rospy.loginfo("pwm_x:"+str(self.pwm_x))

	def backward_cmd(self):
		rospy.loginfo("backward----------------------!!")
		#global vx
		'''while(self.rpm<1 or self.pwm_x != 100):
			self.pwm_x = 100
			self.pub_new_cmd()
			self.pwm_x = 130
			self.pub_new_cmd()
			rospy.Timer(rospy.Duration(0.68), self.callback_backward, oneshot=True)'''
		self.current = rospy.Time.now()
		if self.rpm < 1 and self.pwm_x == 100 and (self.current - self.last_time) == 1:	# backward failed at last time
			
			self.pwm_x = 130
			self.pub_new_cmd()
			self.pwm_x = 100
			self.pub_new_cmd()
			self.pwm_x = 130
			self.pub_new_cmd()
			rospy.Timer(rospy.Duration(0.68), self.callback_backward, oneshot=True)
			self.last_time = rospy.Time.now()

		elif self.rpm >= 1 and self.pwm_x == 100:	# backward continue
			pass

		elif self.pwm_x != 100:		# other situations need reverse motion
			self.pwm_x = 130
			self.pub_new_cmd()
			self.pwm_x = 100
			self.pub_new_cmd()
			self.pwm_x = 130
			self.pub_new_cmd()
			rospy.Timer(rospy.Duration(0.68), self.callback_backward, oneshot=True)
			self.last_time = rospy.Time.now()
		else:		# in case 
			pass
		
	def callback_backward(self, event):
		self.pwm_x = 100
		self.pub_new_cmd()

	def idle(self):
		# global vx
		self.pwm_x = 130
		self.pub_new_cmd()	

	def processing(self):
		#global x
		#global th
		#global vth

		if self.cmd_vth > 0:
			self.pwm_th = (self.conv_th + 16.4882) / 0.71   # 27 + (self.cmd_th/0.25) * 25
	  		if self.pwm_th > 54:
				self.pwm_th = 54
		elif self.cmd_vth < 0:
			self.pwm_th = (self.conv_th + 21.2323) / (0.82)   # 27 - (self.cmd_th/0.39) * 25
			if self.pwm_th < 0:
				self.pwm_th = 0
		else:
			self.pwm_th = 27
		
		if self.cmd_x > 0:
			self.forward_cmd()
		elif self.cmd_x < 0:
			self.backward_cmd()
		else:
			self.idle()

		
		
	def convert_trans_rot_vel_to_steering_angle(self, v, omega, wheelbase):
  		if omega == 0 or v == 0:
    			return 0

  		radius = v / omega
  		return (atan(wheelbase / radius) ) * (180/pi)

	def call_back_sensor(self, data):
		self.rpm = data.data
	
	def callback(self, cmd):
		#global x
		#global th
		self.cmd_x = cmd.linear.x
		self.cmd_vth = cmd.angular.z
		self.conv_th = self.convert_trans_rot_vel_to_steering_angle(self.cmd_x, self.cmd_vth, 0.285)
		#rospy.loginfo("callback_converter:"+str(self.cmd_x)+", " +str(self.cmd_vth)+", " + str(self.conv_th)+ "----------------")

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
    	# rospy.loginfo("I'm in converter!!")
	rospy.sleep(0.05)
    # rospy.spin()
    
  except rospy.ROSInterruptException:
    pass



