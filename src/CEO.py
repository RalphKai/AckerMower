#!/usr/bin/env python

import rospy
import actionlib

from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PoseStamped

def movebase_client():
	
	client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
	
	client.wait_for_server()

	goal = MoveBaseGoal()
	goal.target_pose.header.frame_id = "base_link"
	goal.target_pose.header.stamp = rospy.Time.now()
	
	goal.target_pose.pose.position.x = 2.5

	goal.target_pose.pose.orientation.w = 1.0		# no rotation

	
	client.send_goal(goal)
	wait = client.wait_for_result()
	
	if not wait:
		rospy.logerr("Action server not available!")
		rospy.signal_shutdown("Action server not available!")
	else:
		return client.get_result()

if __name__ == '__main__':
	try:
		rospy.init_node('movebase_client_py')
		result = movebase_client()
		if result:
			rospy.loginfo("Goal execution done!")
	except rospy.ROSInterruptException:
		rospy.loginfo("Navigation test finished.")
