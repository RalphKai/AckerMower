#!/usr/bin/env python
import math
from math import sin, cos, pi
from std_msgs.msg import Float32
import rospy
import tf
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3

rpm = 0.0    # for listener------
pub = rospy.Publisher('odom', Odometry, queue_size=50)
odom = Odometry()
diameter = 8
last_time = 0
speed = 0
x = 0
y = 0
angle = 0

def transfer_odom(rpm, dt):
    speed = (rpm * (diameter * math.pi) / 60)
    # dx = speed * dt
    return speed

def callback(data):
    global speed
    rpm = data.data
    speed = (rpm * (diameter * math.pi) / 60)
    rospy.loginfo(rospy.get_caller_id() + "I get %f", speed)

def callback2(velocity):
    global angle
    angle = velocity.angular.z

def process_data(speed):
    global last_time
    global x
    global y
    # pub.publish(speed)
    if last_time == 0:
        last_time = rospy.Time.now()
        

    current_time = rospy.Time.now()
    dt = (current_time - last_time).to_sec()

    flag = False

    x = x + speed * math.cos(angle) * dt
    y = y + speed * math.sin(angle) * dt
    # dth = 
    odom_quat = tf.transformations.quaternion_from_euler(x, y, angle)
    '''if speed == 0:  
        flag = True

    else:
        flag = False

    if flag and speed == 0:
        continue

    else:'''
    odom.header.stamp = current_time
    odom.header.frame_id = "odom_info"

    odom.pose.pose = Pose(Point(x, y, 0), Quaternion(*odom_quat)) #, Quaternion(*odom_quat)
    #    odom.child_frame_id = "base_link"
    odom.twist.twist = Twist(Vector3(speed, 0, 0), Vector3(0,0,0))
    pub.publish(odom)

    last_time = current_time
    #rospy.sleep()

def listener():
    rospy.init_node("hall_recieve_node", anonymous=True)
    rospy.Subscriber("/hall", Float32, callback)
    rospy.Subscriber("/cmd_vel", Twist, callback2)
    while not rospy.is_shutdown():
    # do whatever you want here
        process_data(speed)
        rospy.sleep(1)
    # while not rospy.is_shutdown():
    # do whatever you want here
    
# -------------------

# for publisher------

'''def talker():
    
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        rospy.loginfo(get_data)
        pub.publish(get_data)
        rate.sleep()'''


if __name__ == '__main__':
    x = 0
    rospy.loginfo('I am in')
    listener()
    # process_data(speed, last_time)
    
    # talker()
