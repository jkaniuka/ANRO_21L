import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Header
from rclpy.clock import ROSClock


class PosePublisher(Node):

    def __init__(self):
        super().__init__('pose_stamped_publisher')
        self.publisher_ = self.create_publisher(PoseStamped, '/tool_position', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)



    def timer_callback(self):
        goal = PoseStamped()
        #goal.header.seq = 1
        goal.header.stamp = ROSClock().now().to_msg()
        goal.header.frame_id = "base_link"

        goal.pose.position.x = 1.0
        goal.pose.position.y = 2.0
        goal.pose.position.z = 0.0

        goal.pose.orientation.x = 0.0
        goal.pose.orientation.y = 0.0
        goal.pose.orientation.z = 0.0
        goal.pose.orientation.w = 1.0


        self.publisher_.publish(goal)
        self.get_logger().info('Publishing: "%s"' % goal)


def main(args=None):
    rclpy.init(args=args)

    pose_stamped_publisher = PosePublisher()

    rclpy.spin(pose_stamped_publisher)
    pose_stamped_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


        

