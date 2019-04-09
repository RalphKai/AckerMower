#!/usr/bin/env python
import roslib
import getch
import rospy
import time
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Int16
import signal

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

left_ultra = 100.0
right_ultra = 100.0 
mode = 0

twist = Twist()
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
rospy.init_node('userToMower')


def callback_mode(data):
	global mode
	mode = data.data

def initial(forward, left, pub, twist):
	twist.linear.x = 130
	twist.angular.z = 26
	pub.publish(twist)

def forward_cmd(forward, left, pub, twist):
	forward = forward_HIGH
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
	forward = 138
	twist.linear.x = forward
	twist.angular.z = left
	pub.publish(twist)
	rospy.sleep(0.3)
	forward = 118
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

def listener_mode():
    	rospy.Subscriber("/mode", Int16, callback_mode)
	
def listener():
    	rospy.Subscriber("/sensing", Float32MultiArray, callback)

def signal_handler(signal, frame):
	print("Ctrl + C, %f", forward_init)
	twist.linear.x = forward_init
	twist.angular.z = left_init
	pub.publish(twist)
	rospy.loginfo(rospy.get_caller_id() + " finish shutdown-----------------")
	exit()

def selfmove(forward, left, pub, twist):
	global mode
	while(mode == 1):
		listener()
		if ( left_ultra >= 30 and right_ultra >=30 ):
			forward, twist = forward_cmd(forward, left, pub, twist)
		else:
			rospy.loginfo(rospy.get_caller_id() + "---------------------")
			forward, twist = pause_cmd(forward, left, pub, twist)
		rospy.sleep(0.1)
		#pub.publish(twist)
                                                                                                                               
def usrmove(forward, left, pub, twist):
	global mode
	global forward_HIGH, forward_init
	rospy.loginfo(rospy.get_caller_id() + "I get mode usr: %d", mode)
	while(mode == 2):
		if mode != 2:
			break
		rospy.loginfo("before getch")
		keyPress = getch.getArrow()
		rospy.loginfo("after getch")
		pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
		rospy.init_node('userToMower')

		twist = Twist()

		if (keyPress == 65) :
			forward = forward_HIGH
		elif (keyPress == 66):
			forward = forward_init
	
		elif (keyPress == 68):
			left += 5
		elif (keyPress == 67):
			left -= 5
		elif (keyPress == 100):
			mode = 0
			break

	# max backward/forward speed is 1.2 m/s

		twist.linear.x = forward
		twist.angular.z = left
		pub.publish(twist)

while not rospy.is_shutdown():			# keyPress != USER_QUIT
	listener_mode()
	rospy.loginfo(rospy.get_caller_id() + "I get mode: %d", mode)
	if mode == 0:
		rospy.loginfo("I in mode0")
		initial(forward, left, pub, twist)
	
	elif mode == 1:
		rospy.loginfo("I in mode1")
		selfmove(forward, left, pub, twist)
	elif mode == 10:
		rospy.loginfo("Over")
		initial(forward, left, pub, twist)
		exit()
	elif mode == 2:
		usrmove(forward, left, pub, twist)
	rospy.sleep(0.5)

	'''rospy.loginfo(rospy.get_caller_id() + "mode: %d", mode)
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	rospy.init_node('userToMower')
	
	twist = Twist()
	listener()
	if ( left_ultra >= 30 and right_ultra >=30 ):
		forward, twist = forward_cmd(forward, left, pub, twist)
	else:
		rospy.loginfo(rospy.get_caller_id() + "---------------------")
		forward, twist = pause_cmd(forward, left, pub, twist)
	rospy.sleep(0.1)'''
	#rospy.loginfo(rospy.get_caller_id() + "I get forward: %f", forward)
	#rospy.loginfo(rospy.get_caller_id() + "I get left_ultra: %f", left_ultra)
	#rospy.loginfo(rospy.get_caller_id() + "I get right_ultra: %f", right_ultra)


'''while(True):			# keyPress != USER_QUIT
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	rospy.init_node('userToMower')
	twist = Twist()
	listener()
	if ( left_ultra >= 30 and right_ultra >=30 ):
		forward, twist = forward_cmd(forward, left, pub, twist)
	else:
		rospy.loginfo(rospy.get_caller_id() + "---------------------")
		forward, twist = pause_cmd(forward, left, pub, twist)
	rospy.sleep(0.1)'''



def shutdown_callback():
	rospy.loginfo(rospy.get_caller_id() + " quit------------------------")
	twist.linear.x = forward_init
	twist.angular.z = left_init
	pub.publish(twist)
	rospy.loginfo(rospy.get_caller_id() + " finish shutdown-----------------")
	exit()

rospy.on_shutdown(shutdown_callback)

'''# signal.signal(signal.SIGINT, signal_handler)
rospy.loginfo(rospy.get_caller_id() + " shutdown------------------------")
twist.linear.x = forward_init
twist.angular.z = left_init
pub.publish(twist)
rospy.loginfo(rospy.get_caller_id() + " finish shutdown-----------------")
rospy.spin()'''
