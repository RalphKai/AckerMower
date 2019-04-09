#!/usr/bin/env python
import getch
import roslib
import rospy
import time
from geometry_msgs.msg import Twist

KEY_UP = 65
KEY_DOWN = 66
KEY_RIGHT = 67
KEY_LEFT = 68
USER_QUIT = 100

MAX_FORWARD = 180
MAX_LEFT = 56
MIN_FORWARD = 100
MIN_LEFT = 0

forward = 130.0
left = 28
keyPress = 0

forward_init = 130.0
left_init = 28
    
forward_HIGH = 150.0

twist = Twist()
twist.linear.x = forward_init
twist.angular.z = left_init
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

rospy.init_node('userToMower')

pub.publish(twist)

while(keyPress != USER_QUIT):
	#pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	#rospy.init_node('userToMower')

	twist = Twist()

	keyPress = getch.getArrow()

	if((keyPress == KEY_UP) and (forward <= MAX_FORWARD)) and forward == forward_init:
		forward = forward_HIGH
		
		left = MIN_LEFT # MIN_LEFT

	elif ((keyPress == KEY_DOWN) and (forward == forward_HIGH)):
		forward = forward_init

	elif ((keyPress == KEY_DOWN) and (forward == forward_init)):
		forward = 135
		twist.linear.x = forward
		twist.angular.z = left
		pub.publish(twist)
                rospy.sleep(0.65)
                forward = 110
                twist.linear.x = forward
		twist.angular.z = left
		pub.publish(twist)
		rospy.sleep(1)
		rospy.loginfo(rospy.get_caller_id() + " ---backward---")
		


	if(left > MAX_LEFT):
		left = MAX_LEFT
	elif(left < MIN_LEFT):
		left = MIN_LEFT

	twist.linear.x = forward
	twist.angular.z = left
	pub.publish(twist)
	

twist.linear.x = forward_init
twist.angular.z = left_init
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
rospy.init_node('userToMower')
twist = Twist()
pub.publish(twist)
rospy.sleep(10)
exit()
