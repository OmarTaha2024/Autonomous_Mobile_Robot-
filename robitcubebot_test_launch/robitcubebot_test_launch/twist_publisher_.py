#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped, Twist
from std_msgs.msg import Header
import sys
import select
import termios
import tty

class PublisherNode(Node):
    def __init__(self):
        super().__init__('twist_publisher_')
        self.declare_parameters(
            namespace='',
            parameters=[
                ('linear_speed', 0.5),
                ('angular_speed', 1.0)
            ]
        )
        self.get_logger().info('Publisher node initialized')
        self.publisher_ = self.create_publisher(TwistStamped, '/robitcubebot_controller/cmd_vel', 10)
        self.old_settings = termios.tcgetattr(sys.stdin)
        self.key_pressed = None
        self.timer_ = self.create_timer(0.1, self.publish_twist)

    def publish_twist(self):
        if self.key_pressed is not None:
            cmd_vel_msg = self.get_keyboard_input()
            twist_msg = TwistStamped()
            twist_msg.header = Header()
            twist_msg.header.stamp = self.get_clock().now().to_msg()
            twist_msg.header.frame_id = ''
            twist_msg.twist = cmd_vel_msg
            self.publisher_.publish(twist_msg)
            self.get_logger().info('Publishing TwistStamped message')

    def get_keyboard_input(self):
        cmd_vel_msg = Twist()
        linear_speed = self.get_parameter('linear_speed').get_parameter_value().double_value
        angular_speed = self.get_parameter('angular_speed').get_parameter_value().double_value
        if self.key_pressed == 'w':
            cmd_vel_msg.linear.x = linear_speed  # Move forward
        elif self.key_pressed == 'x':
            cmd_vel_msg.linear.x = -linear_speed  # Move backward
        elif self.key_pressed == 'a':
            cmd_vel_msg.angular.z = angular_speed  # Turn left
        elif self.key_pressed == 'd':
            cmd_vel_msg.angular.z = -angular_speed  # Turn right
        elif self.key_pressed == 's':  # Spacebar to stop
            cmd_vel_msg.linear.x = 0.0
            cmd_vel_msg.angular.z = 0.0
        self.key_pressed = None
        return cmd_vel_msg

    def keyboard_callback(self):
        try:
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                self.key_pressed = sys.stdin.read(1)
        except Exception as e:
            self.get_logger().error('Error reading keyboard input: {}'.format(str(e)))

    def shutdown_hook(self):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

def main(args=None):
    rclpy.init(args=args)
    publisher_node = PublisherNode()
    try:
        while rclpy.ok():
            rclpy.spin_once(publisher_node, timeout_sec=0.1)
            publisher_node.keyboard_callback()
    except KeyboardInterrupt:
        pass
    finally:
        publisher_node.shutdown_hook()
        publisher_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
