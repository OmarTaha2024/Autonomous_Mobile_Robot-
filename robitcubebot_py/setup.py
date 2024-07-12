from setuptools import find_packages, setup

package_name = 'robitcubebot_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='omar',
    maintainer_email='otaha3911@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "test_publisher = robitcubebot_py.simple_publisher:main",
            "test_odom = robitcubebot_py.odom_publisher:main",
            "test_teleop= robitcubebot_py.teleop_keyboard:main",
            "simple_key_publisher= robitcubebot_py.simple_key_publisher:main",
            "nav2_test= robitcubebot_py.nav2_test:main"
            "gripper_controller= robitcubebot_py.gripper_controller:main",
            "move_group_client= robitcubebot_py.move_group_client:main",

            

        ],
    },
)
