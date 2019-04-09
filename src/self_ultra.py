#!/usr/bin/env python
import getch
import roslib
import rospy

from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
from std_msgs.msg import Float32MultiArray

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

left_ultra = 100.0
right_ultra = 100.0 

flag = False

twist = Twist()
twist.linear.x = forward_init
twist.angular.z = left_init
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
pub2 = rospy.Publisher('/flag', Bool, queue_size=10)
rospy.init_node('userToMower')

pub.publish(twist)
pub2.publish(flag)



def initial(forward, left, pub, twist):
	twist.linear.x = 130
	twist.angular.z = 26
	pub.publish(twist)

def forward_cmd(forward, left, pub, twist):
	forward = forward_forward
	twist.linear.x = forward
	twist.angular.z = left
	pub.publish(twist)
	return forward, twist

def pause_cmd(forward, left, pub, twist):
	forward = 130
	twist.linear.x = forward
	twist.angular.z = left
	pub.publish(twist)
	#rospy.sleep(0.5)
	return forward, twist

def backward_cmd(forward, left, pub, twist):	
	forward = 135
        twist.linear.x = forward
	twist.angular.z = left
        pub.publish(twist)
        rospy.sleep(0.65)
        forward = 110
        twist.linear.x = forward
	twist.angular.z = left
        pub.publish(twist)
       
	return forward, twist

def left_tmp__cmd(forward, left, pub, twist):
	left = MIN_LEFT
	twist.linear.x = forward
	twist.angular.z = MIN_LEFT
	pub.publish(twist)
	rospy.sleep(3)
	left = left_init
	twist.linear.x = forward
	twist.angular.z = left
	pub.publish(twist)

def right_tmp_cmd(forward, left, pub, twist):
	left = MAX_LEFT
	twist.linear.x = forward
	twist.angular.z = left
	pub.publish(twist)
	rospy.sleep(3)
	left = left_init
	twist.linear.x = forward
	twist.angular.z = left
	pub.publish(twist)



def callback(data):
	global left_ultra, right_ultra
	left_ultra = data.data[2]
	right_ultra = data.data[1]

def listener():
    	rospy.Subscriber("/sensing", Float32MultiArray, callback)

def selfmove(forward, left, pub, twist):
	
	while not rospy.is_shutdown():
		listener()
		if ( left_ultra >= 30 and right_ultra >=30 ):
			forward, twist = forward_cmd(forward, left, pub, twist)
		else:
			rospy.loginfo(rospy.get_caller_id() + "---------------------")
			forward, twist = pause_cmd(forward, left, pub, twist)
		rospy.sleep(0.1)
		#pub.publish(twist)
selfmove(forward, left, pub, twist)


def shutdown_callback():
	twist = Twist()
	rospy.loginfo(rospy.get_caller_id() + " quit------------------------")
	flag = True
	twist.linear.x = forward_init
	twist.angular.z = left_init
	pub.publish(twist)
	pub2.publish(flag)
	rospy.loginfo(rospy.get_caller_id() + " finish shutdown-----------------")
	exit()

rospy.on_shutdown(shutdown_callback)
rospy.spin()
