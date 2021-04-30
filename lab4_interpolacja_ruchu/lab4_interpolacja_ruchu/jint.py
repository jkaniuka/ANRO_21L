import sys


# Tutaj również problem z importem serwisu
from lab4_interpolacja_ruchu.srv import Interpolation
import rclpy
from rclpy.node import Node


class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(Interpolation, 'interpolacja')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = AddTwoInts.Request()

    def send_request(self):
        self.req.joint1_goal = float(sys.argv[1])
        self.req.joint2_goal= float(sys.argv[2])
        self.req.joint3_goal = float(sys.argv[3])
        self.req.time_of_move = float(sys.argv[4])
        self.future = self.cli.call_async(self.req)


def main(args=None):
    rclpy.init(args=args)

    minimal_client = MinimalClientAsync()
    minimal_client.send_request()

    while rclpy.ok():
        rclpy.spin_once(minimal_client)
        if minimal_client.future.done():
            try:
                response = minimal_client.future.result()
            except Exception as e:
                minimal_client.get_logger().info(
                    'Service call failed %r' % (e,))
            else:
                minimal_client.get_logger().info(
                    'Result of interpolation for positions: joint1-%d , joint2-%d , joint3-%d in time %d = %d' %
                    (minimal_client.req.joint1_goal, minimal_client.req.joint2_goal, minimal_client.req.joint3_goal, minimal_client.req.time_of_move response.confirmation))
            break

    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()