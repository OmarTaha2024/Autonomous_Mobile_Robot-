import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from moveit_msgs.action import MoveGroup
from sensor_msgs.msg import JointState
from moveit_msgs.msg import Constraints, JointConstraint, RobotState


class MoveGroupClient(Node):

    def __init__(self):
        super().__init__('move_group_client')
        self._action_client = ActionClient(self, MoveGroup, '/move_action')

        self.send_goal()

    def send_goal(self):
        goal_msg = MoveGroup.Goal()

        goal_msg.request.group_name = 'gripper'

        start_state = RobotState()
        joint_state = JointState()
        joint_state.name = ['lift_joint']
        joint_state.position = [0.020]
        start_state.joint_state = joint_state
        goal_msg.request.start_state = start_state

        goal_constraints = Constraints()
        joint_constraint = JointConstraint()
        joint_constraint.joint_name = 'lift_joint'
        joint_constraint.position = 0.0
        goal_constraints.joint_constraints = [joint_constraint]
        goal_msg.request.goal_constraints = [goal_constraints]

        self._action_client.wait_for_server()
        self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info('Received feedback')


def main(args=None):
    rclpy.init(args=args)
    node = MoveGroupClient()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
