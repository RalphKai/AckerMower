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

MAX_FORWARD = 180
MAX_LEFT = 60
MIN_FORWARD = 100
MIN_LEFT = 0

forward_forward = 146
forward_backward = 110
forward = 130.0
left = 26
keyPress = 0

forward_init = 130.0
left_init = 26
    
flag = False

twist = Twist()
twist.linear.x = forward_init
twist.angular.z = left_init
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
pub2 = rospy.Publisher('/flag', Bool, queue_size=10)
rospy.init_node('userToMower')

pub.publish(twist)
pub2.publish(flag)




while(keyPress != USER_QUIT):
	print(forward)
	print(forward == forward_init)

	keyPress = getch.getArrow()

	if((keyPress == KEY_UP) and (forward <= MAX_FORWARD)):
		if forward == forward_init or forward == forward_forward:
			forward = forward_forward
		else:
			forward = forward_init

	elif((keyPress == KEY_DOWN) and (forward >= MIN_FORWARD)):
		if forward == forward_init:
		  forward = 135
                  twist.linear.x = forward
	          twist.angular.z = left
                  pub.publish(twist)
                  rospy.sleep(0.65)
                  forward = 110
                  twist.linear.x = forward
	          twist.angular.z = left
                  pub.publish(twist)
		  twist.linear.x = forward
	          twist.angular.z = left
                  pub.publish(twist)
		else:
		  forward = forward_init
		
	elif((keyPress == KEY_LEFT) and (left <= MAX_LEFT)):
		left += 3
	elif((keyPress == KEY_RIGHT) and (left >= MIN_LEFT)):
		left -= 3

	# max backward/forward speed is 1.2 m/s
	if(forward > MAX_FORWARD):
		forward = MAX_FORWARD
	elif(forward < MIN_FORWARD):
		forward = MIN_FORWARD

	if(left > MAX_LEFT):
		left = MAX_LEFT
	elif(left < MIN_LEFT):
		left = MIN_LEFT

	twist.linear.x = forward
	twist.angular.z = left
	pub.publish(twist)
	rospy.sleep(0.01)

flag = True
twist.linear.x = forward_init
twist.angular.z = left_init
pub.publish(twist)
pub2.publish(flag)
rospy.sleep(1)
exit()
