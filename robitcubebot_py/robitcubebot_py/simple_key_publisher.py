import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
from std_msgs.msg import String  # Change this import

class SerialTransmitterSubscriber(Node):
    def __init__(self):
        super().__init__('serial_transmitter_publisher')
        self.publisher_ = self.create_publisher(String, '/serial_transmitter', 10)
        self.counter_ = 0

        # Initialize subscriber to /robitcubebot_controller/cmd_vel topic
        self.subscription = self.create_subscription(
            TwistStamped,
            '/robitcubebot_controller/cmd_vel',
            self.twist_callback,
            10)
        self.subscription  # prevent unused variable warning

    def twist_callback(self, twistmsg):
        # Extract linear and angular velocities from TwistStamped message
        linear_x = twistmsg.twist.linear.x
        angular_z = twistmsg.twist.angular.z
        self.counter_ += 1
        char_linear =' '
        # Map linear and angular velocities to characters
        if linear_x == 0.5 and angular_z == 0 :
            char_linear = self.map_to_char(linear_x)
        elif linear_x == 0.5 and angular_z == 0.0 :
            char_linear = self.map_to_char(angular_z)
        elif linear_x == 0 and angular_z == 1.0 :
            char_linear = self.map_to_char(angular_z)
        elif linear_x == 0 and angular_z == -1.0 :
            char_linear = self.map_to_char(angular_z)
        elif linear_x == 0.0 and angular_z == 0.0 :
            char_linear = self.map_to_char(linear_x)
        msg = String()
        msg.data = char_linear
        self.publisher_.publish(msg)
        self.get_logger().info(f"publishing #{self.counter_}: {msg}")

    def map_to_char(self, velocity):
        # Map linear and angular velocities to corresponding characters
        if velocity == 0.5:
            return 'w'  # Forward
        elif velocity == -0.5:
            return 'x'  # Backward
        elif velocity == 1.0:
            return 'a'  # Turn left
        elif velocity == -1.0:
            return 'd'  # Turn right
        else:
           return   ' '# Stop


def main(args=None):
    rclpy.init(args=args)
    subscriber_node = SerialTransmitterSubscriber()
    try:
        rclpy.spin(subscriber_node)
    except KeyboardInterrupt:
        pass
    finally:
        subscriber_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
