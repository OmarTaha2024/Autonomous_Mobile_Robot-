import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

class LifterController(Node):
    def __init__(self):
        super().__init__('lifter_controller')
        self.publisher_ = self.create_publisher(Float64, '/lift_joint/command', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = Float64()
        msg.data = 0.01  # Example velocity command
        self.publisher_.publish(msg)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    lifter_controller = LifterController()
    rclpy.spin(lifter_controller)
    lifter_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
