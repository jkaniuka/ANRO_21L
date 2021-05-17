import sys
from interpolation_interfaces.srv import OpInvKin
import rclpy
from rclpy.node import Node


# Struktura wiadomości

# float64 time_of_move
# string type 
# float64 figure_param_a
# float64 figure_param_b
# ---
# string confirmation 


class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(OpInterpolation, 'interpolacja_op')
        while not self.cli.wait_for_service(timeout_sec=2.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = OpInterpolation.Request()

    def send_request(self):
        try:

            # Czas

            if(float(sys.argv[1]) <= 0):
                self.get_logger().info('Niepoprawna wartość czasu')
                raise ValueError("That is not a positive number!")
            else:
                self.req.time_of_move = float(sys.argv[1])


            # Rodzaj trajektorii referencyjnej (prostokąt lub elipsa)

            if(str(sys.argv[2]) !='rectangle' and str(sys.argv[2]) !='ellipse' ):
                self.get_logger().info('Zły typ trajektorii referencyjnej')
                raise ValueError("That is a wrong type!")
            else:
                self.req.type = (sys.argv[2]) 


            if(float(sys.argv[3]) <= 0):
                self.get_logger().info('Niepoprawna wartość parametru a figury')
                raise ValueError("That is not a positive number!")
            else:
                self.req.time_of_move = float(sys.argv[3])

            if(float(sys.argv[4]) <= 0):
                self.get_logger().info('Niepoprawna wartość parametru b figury')
                raise ValueError("That is not a positive number!")
            else:
                self.req.time_of_move = float(sys.argv[4]) 
        except IndexError:
            print("Niepoprawna liczba parametrów")
            raise Exception()
        except ValueError:
            print("Błędne parametry")
            raise Exception()
            
        self.future = self.cli.call_async(self.req)



def main(args=None):
    rclpy.init(args=args)

    try:

        minimal_client = MinimalClientAsync()
        minimal_client.send_request()
    except:
        print("Anulowanie realizacji zapytania")
    else:


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
                        'Result of interpolation in time %d, trajectory type- %d , params a = %d, b= is %s' %
                        (minimal_client.req.time_of_move, minimal_client.req.type, minimal_client.req.figure_param_a, minimal_client.req.figure_param_b, response.confirmation))
                    return
    finally:
        minimal_client.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()