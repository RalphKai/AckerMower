## Main launch file
Launch the system with several launch files to get different functions.

## Navigation
```
roslaunch mower arduino_part.launch  # rosserial
roslaunch mower D435_tolaser.launch  # convert 3D depthImage to 2D laserscan
roslaunch mower dwa.launch           # main function
```

## SLAM
```
roslaunch mower auduino_part.launch  # rosserial
rosrun mower keyboard.py            # remote controller
roslaunch mower drive_gmapping.launch  # gmapping
```

## Test Motion Model without AMCL
```
roslaunch mower arduino_part.launch  # rosserial
roslaunch mower ackmower_withoutamcl.launch  # just launch EKF node
