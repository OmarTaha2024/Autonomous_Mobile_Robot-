import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.actions import GroupAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.substitutions import TextSubstitution
from launch_ros.actions import Node
from launch_ros.actions import PushRosNamespace
from ament_index_python.packages import get_package_share_directory
from ament_index_python.packages import get_package_share_path
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command

def generate_launch_description():


    world_file_name = 'my_world.world'
    world = os.path.join(
        get_package_share_directory('robitcubebot_bringup'),
        'worlds',
        world_file_name
    )
    gazebo = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("robitcubebot_description"),
            "launch",
            "gazebo.launch.py"
        ),
        launch_arguments={'world': world}.items()
    )
    rviz_config_path = os.path.join(get_package_share_directory('robitcubebot_description'),
                                    'rviz', 'my_robot_config.rviz')
    
    controller = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("robitcubebot_controller"),
            "launch",
            "controller.launch.py"
        ),
        launch_arguments={
            "use_simple_controller": "False",
            "use_python": "False"
        }.items(),
    )
    rviz2_node = Node(
        package="rviz2",
        executable="rviz2",
        arguments=['-d', rviz_config_path]
    )

    moveit = IncludeLaunchDescription(
           os.path.join(
              get_package_share_directory("robitcubebot_moveit"),
               "launch",
              "moveit.launch.py"
           ),
           launch_arguments={"is_sim": "True"}.items()
       )

    
    return LaunchDescription([
        gazebo,
        controller,
        rviz2_node,
        moveit,
    ])
