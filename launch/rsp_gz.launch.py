import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription

# from launch.substitutions import LaunchConfiguration
from launch.actions import (
    IncludeLaunchDescription,
    RegisterEventHandler,
    ExecuteProcess,
)
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg_name = "anna"

    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(
                    get_package_share_directory(pkg_name), "launch", "rsp.launch.py"
                )
            ]
        ),
        launch_arguments={"use_sim_time": "true"}.items(),
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(
                    get_package_share_directory("gazebo_ros"),
                    "launch",
                    "gazebo.launch.py",
                )
            ]
        ),
    )

    spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=["-topic", "robot_description", "-entity", "anna"],
        output="screen",
    )

    joint_state_broadcaster_spawn = ExecuteProcess(
        cmd=[
            "ros2",
            "control",
            "load_controller",
            "--set-state",
            "active",
            "joint_state_broadcaster",
        ],
        output="screen",
    )

    diff_drive_spawner = ExecuteProcess(
        cmd=[
            "ros2",
            "control",
            "load_controller",
            "--set-state",
            "active",
            "diff_drive_base_controller",
        ],
        output="screen",
    )

    camera_controller_spawner = ExecuteProcess(
        cmd=[
            "ros2",
            "control",
            "load_controller",
            "--set-state",
            "active",
            "camera_controller",
        ],
        output="screen",
    )

    position_goals = PathJoinSubstitution(
        [
            FindPackageShare("line_follow_robot_description"),
            "config",
            "forward_command_controller_publisher.yaml",
        ]
    )

    forward_position_controller_publisher_node = Node(
        package="ros2_controllers_test_nodes",
        executable="publisher_forward_position_controller",
        parameters=[position_goals],
        output="screen",
    )
    return LaunchDescription(
        [
            rsp,
            gazebo,
            spawn_entity,
            RegisterEventHandler(
                event_handler=OnProcessExit(
                    target_action=spawn_entity, on_exit=[joint_state_broadcaster_spawn]
                )
            ),
            RegisterEventHandler(
                event_handler=OnProcessExit(
                    target_action=joint_state_broadcaster_spawn,
                    on_exit=[diff_drive_spawner],
                )
            ),
            RegisterEventHandler(
                event_handler=OnProcessExit(
                    target_action=diff_drive_spawner,
                    on_exit=[camera_controller_spawner],
                )
            ),
            # forward_position_controller_publisher_node,
        ]
    )
