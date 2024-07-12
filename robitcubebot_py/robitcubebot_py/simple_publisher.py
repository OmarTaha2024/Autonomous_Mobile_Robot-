import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SerialTransmitterPublisher(Node):
    def __init__(self):
        super().__init__('serial_transmitter_publisher')
        self.publisher_ = self.create_publisher(String, '/serial_transmitter', 10)
        self.timer_ = self.create_timer(1.0, self.publish_message)
        self.counter_ = 0

    def publish_message(self):
        self.counter_ += 1
        msg = String()
        msg.data = 'w'
        self.publisher_.publish(msg)
        self.get_logger().info(f"publishing #{self.counter_}: {msg}")

def main(args=None):
    rclpy.init(args=args)
    transmitter_publisher = SerialTransmitterPublisher()
    rclpy.spin(transmitter_publisher)
    transmitter_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

