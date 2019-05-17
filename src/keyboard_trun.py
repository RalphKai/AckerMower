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
MAX_LEFT = 60

MIN_FORWARD = 100
MIN_LEFT = 0

forward = 130.0
left = 30
keyPress = 0

forward_init = 130.0
left_init = 30
    

forward_HIGH = 145.0

twist = Twist()
twist.linear.x = forward_init
twist.angular.z = left_init
pub = rospy.Publisher('/cmd_vel_toMotor', Twist, queue_size=10)

rospy.init_node('userToMower')

pub.publish(twist)

def callback(event):
	forward = 100
        twist.linear.x = forward
	twist.angular.z = left
	pub.publish(twist)
	rospy.loginfo(rospy.get_caller_id() + " ---backward---")

while(keyPress != USER_QUIT):
	#pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	#rospy.init_node('userToMower')

	twist = Twist()

	keyPress = getch.getArrow()

	if((keyPress == KEY_UP) and (forward <= MAX_FORWARD)) and forward == forward_init:
		forward = forward_HIGH
		
		left = MAX_LEFT # MIN_LEFT
	# elif ((keyPress == KEY_UP) and (forward <= MAX_FORWARD)) and forward == forward_init:

	elif ((keyPress == KEY_DOWN) and (forward == forward_HIGH)):
		forward = forward_init

	elif ((keyPress == KEY_DOWN) and (forward == forward_init)):
		forward = 100
		twist.linear.x = forward
		twist.angular.z = left
		pub.publish(twist)
		forward = 130.5
		twist.linear.x = forward
		twist.angular.z = left
		pub.publish(twist)
		rospy.Timer(rospy.Duration(0.68), callback, oneshot=True)
		
	else:
		forward = forward_init


	if(left > MAX_LEFT):
		left = MAX_LEFT
	elif(left < MIN_LEFT):
		left = MIN_LEFT

	twist.linear.x = forward
	twist.angular.z = left
	pub.publish(twist)
	


twist.linear.x = forward_init
twist.angular.z = left_init
pub = rospy.Publisher('/cmd_vel_toMower', Twist, queue_size=10)
rospy.init_node('userToMower')
twist = Twist()
pub.publish(twist)
rospy.sleep(10)
exit()












