#!/usr/bin/env python

import rospy
import actionlib

from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Pose, Point, Quaternion
from tf.transformations import quaternion_from_euler

class GoalPointer():
	def __init__(self):
		rospy.init_node('movebase_client')
		rospy.on_shutdown(self.shutdownhook)
		self.waypoint = Pose(Point(2.5, 0.0, 0.0),Quaternion(*quaternion_from_euler(0.0,0.0,0.0)) )
		self.init_marker()	
	
	def init_marker(self):
		# Set up our waypoint markers   
		marker_scale = 0.2  
		marker_lifetime = 0 # 0 is forever  
		marker_ns = 'waypoints'  
		marker_id = 0  
		marker_color = {'r': 1.0, 'g': 0.7, 'b': 1.0, 'a': 1.0}  
	 
		# Define a marker publisher.  
		self.marker_pub = rospy.Publisher('waypoint_markers', Marker, queue_size=10)  
	 
		# Initialize the marker points list.  
		self.markers = Marker()  
		self.markers.ns = 'waypoints'  
		self.markers.id = marker_id  
		self.markers.type = Marker.SPHERE
		self.markers.action = Marker.ADD  
		self.markers.lifetime = rospy.Duration(marker_lifetime)  
		self.markers.scale.x = marker_scale  
		self.markers.scale.y = marker_scale  
		self.markers.color.r = marker_color['r']  
		self.markers.color.g = marker_color['g']  
		self.markers.color.b = marker_color['b']  
		self.markers.color.a = marker_color['a']  
	 
		self.markers.header.frame_id = 'map_amcl'  
		self.markers.header.stamp = rospy.Time.now()  
		self.markers.points = list()  
	
	
	def movebase_client(self):

		client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
	
		client.wait_for_server()

		goal = MoveBaseGoal()
		goal.target_pose.header.frame_id = "base_link"
		goal.target_pose.header.stamp = rospy.Time.now()
	
		goal.target_pose.pose.position.x = 2.5

		goal.target_pose.pose.orientation.w = 1.0		# no rotation
		p = Point()
		p = self.waypoint.position
		self.markers.points.append(p)

		client.send_goal(goal)
		wait = client.wait_for_result()
		self.marker_pub.publish(self.markers)
		if not wait:
			rospy.logerr("Action server not available!")
			rospy.signal_shutdown("Action server not available!")
		else:
			return client.get_result()

	def shutdownhook(self):
		rospy.loginfo(rospy.get_caller_id() + " stop")

if __name__ == '__main__':
	try:
		move_base_goal = GoalPointer()
		result = move_base_goal.movebase_client()
		if result:
			rospy.loginfo("Goal execution done!")
	except rospy.ROSInterruptException:
		rospy.loginfo("Navigation test finished.")
