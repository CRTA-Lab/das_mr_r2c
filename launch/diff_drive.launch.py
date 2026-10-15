from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, RegisterEventHandler
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessExit
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg = FindPackageShare('das_mr_r2c')

    use_rviz = LaunchConfiguration('rviz')
    use_teleop = LaunchConfiguration('teleop')

    robot_description = {
        'robot_description': ParameterValue(
            Command(['xacro ', PathJoinSubstitution(
                [pkg, 'urdf', 'diff_drive', 'diff_drive_robot.urdf.xacro'])]),
            value_type=str)
    }
    controllers_yaml = PathJoinSubstitution([pkg, 'config', 'diff_drive', 'diff_drive_controllers.yaml'])
    rviz_config = PathJoinSubstitution([pkg, 'rviz', 'mobile_robot.rviz'])

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[robot_description],
        output='screen',
    )

    control_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[controllers_yaml],
        remappings=[
            ('~/robot_description', '/robot_description'),
            ('/diff_drive_controller/cmd_vel', '/cmd_vel'),            
            ('/diff_drive_controller/cmd_vel_unstamped', '/cmd_vel'),
        ],
        output='screen',
    )

    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
    )

    diff_drive_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['diff_drive_controller', '--controller-manager', '/controller_manager'],
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config],
        condition=IfCondition(use_rviz),
        output='log',
    )

    delay_diff_drive = RegisterEventHandler(
        OnProcessExit(target_action=joint_state_broadcaster_spawner,
                      on_exit=[diff_drive_controller_spawner]))

    return LaunchDescription([
        DeclareLaunchArgument('rviz', default_value='true', description='Start RViz2'),
        DeclareLaunchArgument('teleop', default_value='true',
                              description='Start teleop_twist_keyboard in an xterm window'),
        robot_state_publisher,
        control_node,
        joint_state_broadcaster_spawner,
        delay_diff_drive,
        rviz,
    ])
