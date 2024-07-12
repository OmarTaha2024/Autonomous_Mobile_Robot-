import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    # Specify the path to the parameter file
    twist_params_file = os.path.join(
        get_package_share_directory('robitcubebot_test_launch'),
        'config',
        'twist_params.yaml'
    )

    return LaunchDescription([
        Node(
            package='robitcubebot_test_launch',
            executable='twist_publisher_.py',
            name='twist_publisher_',
            output='screen',
            parameters=[twist_params_file]
        )
    ])
