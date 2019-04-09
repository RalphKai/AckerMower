#!/usr/bin/env python
import getch
import roslib
import rospy

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
left = 26
keyPress = 0

forward_init = 130.0
left_init = 26
    
forward_HIGH = 146.0

twist = Twist()
twist.linear.x = forward_init
twist.angular.z = left_init
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
rospy.init_node('userToMower')

pub.publish(twist)

while(keyPress != USER_QUIT):
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	rospy.init_node('userToMower')

	twist = Twist()

	keyPress = getch.getArrow()

	if((keyPress == KEY_UP) and (forward <= MAX_FORWARD)) and forward == forward_init:
		forward = forward_HIGH
	elif((keyPress == KEY_DOWN) and (forward >= MIN_FORWARD)) and forward == forward_HIGH:
		forward = forward_init
	
	'''elif((keyPress == KEY_LEFT) and (left <= MAX_LEFT)):
		left += 5
	elif((keyPress == KEY_RIGHT) and (left >= MIN_LEFT)):
		left -= 5'''


	if((keyPress == KEY_LEFT) and (left == left_init)):
		left = MAX_LEFT
	elif((keyPress == KEY_RIGHT) and (left == MAX_LEFT)):
		left = left_init
	elif((keyPress == KEY_RIGHT) and (left == left_init)):
		left = MIN_LEFT
	elif((keyPress == KEY_LEFT) and (left == MIN_LEFT)):
		left = left_init

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
	#rospy.sleep(0.5)


twist.linear.x = forward_init
twist.angular.z = left_init
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
rospy.init_node('userToMower')
twist = Twist()
pub.publish(twist)
rospy.sleep(10)
exit()
