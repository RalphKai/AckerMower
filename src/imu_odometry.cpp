#include <ros/ros.h>
#include <tf/transform_broadcaster.h>
#include <nav_msgs/Odometry.h>
#include <sensor_msgs/Imu.h>

double linear_ax, linear_ay, linear_az, gyro_x, gyro_y, gyro_z;

void imuCallback(const sensor_msgs::Imu::ConstPtr &msg){
  linear_ax = msg->linear_acceleration.x;
  linear_ay = msg->linear_acceleration.y;
  linear_az = msg->linear_acceleration.z;
  gyro_x = msg->angular_velocity.x;
  gyro_y = msg->angular_velocity.y;
  gyro_z = msg->angular_velocity.z;

  //printf("gyro_x: %f", gyro_x);
  //printf("gyro_y: %f", gyro_y);
  //printf("gyro_z: %f", gyro_z);

}


int main(int argc, char** argv){
  ros::init(argc, argv, "odometry_publisher");

  ros::NodeHandle n;
  ros::Publisher odom_pub = n.advertise<nav_msgs::Odometry>("odom", 50);
  ros::Subscriber imu_info = n.subscribe<sensor_msgs::Imu>("/imu", 1000, imuCallback);
  tf::TransformBroadcaster odom_broadcaster;

  double x = 0.0;
  double y = 0.0;
  double z = 0.0;

  double ax = linear_ax;
  double ay = linear_ay;
  double az = gyro_z;
  double ax_last = linear_ax;
  double ay_last = linear_ay;
  double az_last = gyro_z;
  ros::Time current_time, last_time;
  current_time = ros::Time::now();
  last_time = ros::Time::now();

  ros::Rate r(1);
  while(ros::ok()){
    
    ros::spinOnce();               // check for incoming messages
    current_time = ros::Time::now();
    ax_last = ax;
    ay_last = ay;
    az_last = az;
    ax = linear_ax;
    ay = linear_ay;
    az = linear_az;
    //compute odometry in a typical way given the velocities of the robot
    double dt = (current_time - last_time).toSec();
    double vz = (az - az_last) * dt;
    double delta_z = vz * dt;
    z += delta_z;

    double vx = (ax - ax_last) * dt;
    double vy = (ay - ay_last) * dt;
    double delta_x = (vx * cos(z) - vy * sin(z)) * dt;
    double delta_y = (vx * sin(z) + vy * cos(z)) * dt;
    
    x += delta_x;
    y += delta_y;
    

    //since all odometry is 6DOF we'll need a quaternion created from yaw
    geometry_msgs::Quaternion odom_quat = tf::createQuaternionMsgFromYaw(z);

    //first, we'll publish the transform over tf
    geometry_msgs::TransformStamped odom_trans;
    odom_trans.header.stamp = current_time;
    odom_trans.header.frame_id = "odom";
    odom_trans.child_frame_id = "base_link";

    odom_trans.transform.translation.x = x;
    odom_trans.transform.translation.y = y;
    odom_trans.transform.translation.z = z;
    odom_trans.transform.rotation = odom_quat;

    //send the transform
    odom_broadcaster.sendTransform(odom_trans);

    //next, we'll publish the odometry message over ROS
    nav_msgs::Odometry odom;
    odom.header.stamp = current_time;
    odom.header.frame_id = "odom";

    //set the position
    odom.pose.pose.position.x = x;
    odom.pose.pose.position.y = y;
    odom.pose.pose.position.z = z;
    odom.pose.pose.orientation = odom_quat;

    //set the velocity
    odom.child_frame_id = "base_link";
    odom.twist.twist.linear.x = vx;
    odom.twist.twist.linear.y = vy;
    odom.twist.twist.angular.z = vz;

    //publish the message
    odom_pub.publish(odom);

    last_time = current_time;
    r.sleep();
  }
}
