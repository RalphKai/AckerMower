#!/usr/bin/env python
import getch
import roslib
import rospy

from geometry_msgs.msg import Twist
from std_msgs.msg import Bool

KEY_UP = 65
KEY_DOWN = 66
KEY_RIGHT = 67
KEY_LEFT = 68
USER_QUIT = 100
keyPress = 0
vx = 0
vth = 0
twist = Twist()
twist.linear.x = 0
twist.angular.z = 0

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

rospy.init_node('userToMower')

pub.publish(twist)

while(keyPress != USER_QUIT):

	keyPress = getch.getArrow()

	if((keyPress == KEY_UP) and (twist.linear.x == 0)):
		twist.linear.x = 0.25

	elif((keyPress == KEY_UP) and (twist.linear.x == -0.1)):
		twist.linear.x = 0

	elif((keyPress == KEY_DOWN) and (twist.linear.x == 0.25)):
		twist.linear.x = 0

	elif(keyPress == KEY_DOWN) and (twist.linear.x == 0):
		twist.linear.x = -0.1
		
	if((keyPress == KEY_LEFT)):
		twist.angular.z = twist.angular.z + 0.1
		if twist.angular.z >= 0.2:
			twist.angular.z = 0.2
	elif((keyPress == KEY_RIGHT)):
		twist.angular.z = twist.angular.z - 0.1
		if twist.angular.z <= -0.2:
			twist.angular.z = -0.2
	pub.publish(twist)
	rospy.sleep(0.01)


twist.linear.x = 0
twist.angular.z = 0
pub.publish(twist)

