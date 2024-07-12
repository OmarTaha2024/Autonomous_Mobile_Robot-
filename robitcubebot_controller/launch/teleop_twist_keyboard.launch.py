from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
import os

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='robitcubebot_controller',  
            executable='teleop_publisher',
            name='teleop_publisher',
            output='screen',
            parameters=[os.path.join(
                get_package_share_directory("robitcubebot_controller"), 'config', 'key_teleop.yaml')]
        )
    ])
