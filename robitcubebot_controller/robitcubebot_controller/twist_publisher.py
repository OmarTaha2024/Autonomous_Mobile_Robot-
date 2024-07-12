#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped, Twist
from std_msgs.msg import Header
import sys, select, termios, tty

class PublisherNode(Node):
    def __init__(self):
        super().__init__('teleop_publisher')
        self.publisher_ = self.create_publisher(TwistStamped, '/robitcubebot_controller/cmd_vel', 10)
        self.timer_ = self.create_timer(0.1, self.publish_twist)
        self.get_logger().info('Publisher node initialized')
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())

    def publish_twist(self):
        twist_msg = TwistStamped()
        twist_msg.header = Header()
        twist_msg.header.stamp = self.get_clock().now().to_msg()
        twist_msg.header.frame_id = ''

        twist_msg.twist = self.get_keyboard_input()

        self.publisher_.publish(twist_msg)
        self.get_logger().info('Publishing TwistStamped message')

    def get_keyboard_input(self):
        key = None
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            key = sys.stdin.read(1)
        cmd_vel_msg = Twist()
        if key == 'w':
            cmd_vel_msg.linear.x = 0.5  # Move forward
            cmd_vel_msg.angular.z = 0.0
        elif key == 'x':
            cmd_vel_msg.linear.x = -0.5  # Move backward
            cmd_vel_msg.angular.z = 0.0
        elif key == 'a':
            cmd_vel_msg.linear.x = 0.0
            cmd_vel_msg.angular.z = 1.0  # Turn left
        elif key == 'd':
            cmd_vel_msg.linear.x = 0.0
            cmd_vel_msg.angular.z = -1.0  # Turn right
        elif key == 's':  # Spacebar to stop
            cmd_vel_msg.linear.x = 0.0
            cmd_vel_msg.angular.z = 0.0
        return cmd_vel_msg

def main(args=None):
    rclpy.init(args=args)
    publisher_node = PublisherNode()
    try:
        rclpy.spin(publisher_node)
    except KeyboardInterrupt:
        pass
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, publisher_node.old_settings)
        publisher_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
