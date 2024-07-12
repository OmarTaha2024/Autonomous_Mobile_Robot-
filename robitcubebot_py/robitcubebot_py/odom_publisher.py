import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
from builtin_interfaces.msg import Time
from std_msgs.msg import Header
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3

class PublisherNode(Node):
    def __init__(self):
        super().__init__('twist_publisher')
        self.publisher_ = self.create_publisher(TwistStamped, '/robitcubebot_controller/cmd_vel', 10)
        self.timer_ = self.create_timer(1, self.publish_twist)
        self.get_logger().info('Publisher node initialized')

    def publish_twist(self):
        twist_msg = TwistStamped()
        twist_msg.header = Header()
        twist_msg.header.stamp = Time()
        twist_msg.header.frame_id = ''

        twist_msg.twist = Twist()
        twist_msg.twist.linear = Vector3(x=0.5, y=0.0, z=0.0)
        twist_msg.twist.angular = Vector3(x=0.0, y=0.0, z=0.5)

        self.publisher_.publish(twist_msg)
        self.get_logger().info('Publishing TwistStamped message')

def main(args=None):
    rclpy.init(args=args)
    publisher_node = PublisherNode()
    try:
        rclpy.spin(publisher_node)
    except KeyboardInterrupt:
        pass
    publisher_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
