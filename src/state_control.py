#!/usr/bin/env python
import getch
import roslib
import rospy

from std_msgs.msg import Int16

KEY_selfmove = '1'
KEY_usercontrol = '2'
#KEY_settle = 67
KEY_settle = '3'
USER_QUIT = 100

mode = Int16()
last = 0
mode.data = 0
pub = rospy.Publisher('/mode', Int16, queue_size=10)
rospy.init_node('state_control')
pub.publish(mode)

keyPress = getch.getch()
while(keyPress != 'q'):
	pub = rospy.Publisher('/mode', Int16, queue_size=10)
	rospy.init_node('state_control')
	mode = Int16()
	keyPress = getch.getch()
	mode.data = last
	if (keyPress == KEY_selfmove):
		last = 1
		mode.data = 1		# 
	elif(keyPress == KEY_usercontrol):
		last = 2
		mode.data = 2
	elif(keyPress == KEY_settle):
		last = 0
		mode.data = 0
	elif(keyPress == '4'):
		last = 10
		mode.data = 10
	pub.publish(mode)
	rospy.sleep(0.5)

mode.data = 0
pub = rospy.Publisher('/mode', Int16, queue_size=10)
rospy.init_node('state_control')
pub.publish(mode)
rospy.sleep(1)
exit()
