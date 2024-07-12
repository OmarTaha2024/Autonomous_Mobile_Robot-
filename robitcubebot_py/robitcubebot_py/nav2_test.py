import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TwistStamped
from std_msgs.msg import Header

class CmdVelRepublisher(Node):

    def __init__(self):
        super().__init__('cmd_vel_republisher')
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10)
        self.publisher = self.create_publisher(
            TwistStamped,
            '/robitcubebot_controller/cmd_vel',
            10)
        self.get_logger().info('CmdVelRepublisher node is running.')

    def cmd_vel_callback(self, msg):
        # Create a TwistStamped message
        stamped_msg = TwistStamped()
        stamped_msg.header = Header()
        stamped_msg.header.stamp = self.get_clock().now().to_msg()  # Set current time
        stamped_msg.twist = msg  # Assign the Twist message to TwistStamped

        # Publish the TwistStamped message
        self.publisher.publish(stamped_msg)

def main(args=None):
    rclpy.init(args=args)
    cmd_vel_republisher = CmdVelRepublisher()
    rclpy.spin(cmd_vel_republisher)
    cmd_vel_republisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
