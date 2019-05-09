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

def callback1(event):
	global twist
	global pub
	twist.linear.x = 0.25
	twist.angular.z = 0.2
	pub.publish(twist)
	rospy.Timer(rospy.Duration(2.5), callback2, oneshot=True)
	
def callback2(event):
	global twist
	global pub
	twist.linear.x = 0.25
	twist.angular.z = -0.2
	pub.publish(twist)
	rospy.Timer(rospy.Duration(2.5), callback3, oneshot=True)

def callback3(event):
	global twist
	global pub
	twist.linear.x = 0.25
	twist.angular.z = 0
	pub.publish(twist)
	rospy.Timer(rospy.Duration(2), callback4, oneshot=True)

def callback4(event):
	global twist
	global pub
	twist.linear.x = 0
	twist.angular.z = 0
	pub.publish(twist)
	

while(keyPress != USER_QUIT):

	keyPress = getch.getArrow()

	if((keyPress == KEY_UP) and (twist.linear.x == 0)):
		twist.linear.x = 0.25
		twist.angular.z = 0
		pub.publish(twist)
		rospy.Timer(rospy.Duration(10), callback4, oneshot=True)
		'''twist.linear.x = 0.25
		twist.angular.z = 0.2
		pub.publish(twist)
		rospy.sleep(2.5)
		twist.linear.x = 0.25
		twist.angular.z = -0.2
		pub.publish(twist)
		rospy.sleep(2.5)
		twist.linear.x = 0.25
		twist.angular.z = 0
		pub.publish(twist)
		rospy.sleep(3)
		twist.linear.x = 0
		twist.angular.z = 0
		pub.publish(twist)'''

twist.linear.x = 0
twist.angular.z = 0
pub.publish(twist)

