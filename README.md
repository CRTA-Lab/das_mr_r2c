# das_mr_r2c

## Build
```bash
mkdir -p pas_r2c_ws/src
git clone https://github.com/CRTA-Lab/das_mr_r2c.git
cd ~/pas_r2c_ws
colcon build --packages-select das_mr_r2c
source install/setup.bash
```

## Diff drive
```bash
ros2 launch das_mr_r2c diff_drive.launch.py
```
Keyboard control:
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p stamped:=true
```

Data flow:
```
teleop (TwistStamped /cmd_vel) -> diff_drive_controller (inverse kinematics)
  -> left/right_wheel_joint/velocity commands -> mock hardware integrates position
  -> wheel position/velocity states -> diff_drive_controller (forward kinematics / odometry)
  -> /diff_drive_controller/odom + TF odom->base_footprint  -> RViz
  -> joint_state_broadcaster -> /joint_states -> robot_state_publisher -> wheel TF (wheels spin)
```

Useful commands:
```bash
ros2 control list_controllers
ros2 control list_hardware_interfaces
ros2 topic echo /diff_drive_controller/odom
```

## Ackermann
```bash
ros2 launch das_mr_r2c ackermann.launch.py
```
Keyboard control:
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

Data flow:
```
teleop (Twist /cmd_vel) -> ackermann_steering_controller (inverse kinematics)
  -> rear_*_wheel_joint/velocity + front_*_steering_joint/position commands -> mock hardware
  -> wheel position + steering position states -> ackermann_steering_controller (odometry)
  -> /ackermann_steering_controller/odometry + TF odom->base_footprint -> RViz
  -> joint_state_broadcaster -> /joint_states -> robot_state_publisher -> wheel/steering TF
```

Useful commands:
```bash
ros2 control list_controllers
ros2 control list_hardware_interfaces
ros2 topic echo /ackermann_steering_controller/odometry
```

## Mecanum
```bash
ros2 launch das_mr_r2c mecanum.launch.py
```
Keyboard control (hold Shift for sideways motion):
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

Data flow:
```
teleop (Twist /cmd_vel) -> mecanum_drive_controller (inverse kinematics)
  -> 4x *_wheel_joint/velocity commands -> mock hardware integrates position
  -> wheel velocity states -> mecanum_drive_controller (forward kinematics / odometry)
  -> /mecanum_drive_controller/odometry + TF odom->base_footprint -> RViz
  -> joint_state_broadcaster -> /joint_states -> robot_state_publisher -> wheel TF (wheels spin)
```

Useful commands:
```bash
ros2 control list_controllers
ros2 control list_hardware_interfaces
ros2 topic echo /mecanum_drive_controller/odometry
```
