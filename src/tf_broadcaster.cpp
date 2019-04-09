#include <ros/ros.h>
#include <tf/transform_broadcaster.h>

int main(int argc, char** argv){
  ros::init(argc, argv, "mower_tf_publisher");
  ros::NodeHandle nh;

  ros::Rate r(30);

  tf::TransformBroadcaster base_to_laser_broadcaster;

  while(nh.ok()){
    base_to_laser_broadcaster.sendTransform(
      tf::StampedTransform(
        tf::Transform(tf::Quaternion(0, 0, 0, 1), tf::Vector3(0, 0, 0)),
        ros::Time::now(),"base_link", "scan"));
    base_to_laser_broadcaster.sendTransform( 
      tf::StampedTransform(
        tf::Transform(tf::Quaternion(0, 0, 0, 1), tf::Vector3(0, 0, 0)),
        ros::Time::now(),"scan", "camera_link"));
    r.sleep();
  }
}
