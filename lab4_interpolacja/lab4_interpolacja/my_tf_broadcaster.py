import rclpy
from std_msgs.msg import String
from tf2_msgs.msg import TFMessage 
from rclpy.clock import ROSClock
from geometry_msgs.msg import Quaternion
import tf2_ros
import geometry_msgs.msg
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
import math



class MinimalPublisher(Node):

	def __init__(self):
		super().__init__('minimal_publisher')
		self.pose_publisher = self.create_publisher(PoseStamped, '/cartesian', 10)
		timer_period = 0.5  # seconds
		self.timer = self.create_timer(timer_period, self.timer_callback)
		self.i = 0

	def timer_callback(self):

		poses = PoseStamped()
		now = self.get_clock().now()
		poses.header.stamp = ROSClock().now().to_msg()
		poses.header.frame_id = "base_frame"
		poses.pose.position.x = 5.0*math.sin(self.i*3)
		poses.pose.position.y = 5.0*math.cos(self.i*2)
		poses.pose.position.z = 3.0
		poses.pose.orientation = Quaternion(w=float(1.0), x=float(1.0), y=float(1.0), z=float(1.0))
		self.pose_publisher.publish(poses)
		self.i += 1




	


def main(args=None):
	rclpy.init(args=args)

	minimal_publisher = MinimalPublisher()
	rclpy.spin(minimal_publisher)

	minimal_publisher.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
	main()


