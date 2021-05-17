import sys
from interpolation_interfaces.srv import OpInvKin
import rclpy
from rclpy.node import Node


class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(OpInterpolation, 'interpolacja_op')
        while not self.cli.wait_for_service(timeout_sec=2.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = OpInterpolation.Request()

    def send_request(self):
        try:

            # Zadane położenie w przestrzeni kartezjańskiej

            # Baza ma wysokość 1m + człon1 też ma 1m
             if(not(float(sys.argv[1]) >= 1 & float(sys.argv[1])<= 2)):
                self.get_logger().info('Położenie nieosiągalne')
                raise ValueError("Position out of range!")
            else:
                self.req.x_goal = float(sys.argv[1])
                
            # Długość członu 2 to 3m
            if(not(float(sys.argv[2]) >= -3 & float(sys.argv[2])<=0)):
                self.get_logger().info('Położenie nieosiągalne')
                raise ValueError("Position out of range!")
            else:
                self.req.y_goal= float(sys.argv[2])

            # Długość członu 3. to 2m
            if(not(float(sys.argv[3]) >= 0 & float(sys.argv[3]) <= 2)):
                self.get_logger().info('Położenie nieosiągalne')
                raise ValueError("Position out of range!")
            else:
                self.req.z_goal = float(sys.argv[3])



            # Czas

            if(float(sys.argv[4]) <= 0):
                self.get_logger().info('Niepoprawna wartość czasu')
                raise ValueError("That is not a positive number!")
            else:
                self.req.time_of_move = float(sys.argv[4])


            # Rodzaj trajektorii referencyjnej (prostokąt lub elipsa)

            if(str(sys.argv[5]) !='rectangle' and str(sys.argv[5]) !='ellipse' ):
                self.get_logger().info('Zły typ trajektorii referencyjnej')
                raise ValueError("That is a wrong type!")
            else:
                self.req.type = (sys.argv[5])  
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
                        'Result of interpolation for positions: x = %d , y = %d , z = %d, in time %d, trajectory - %d is %s' %
                        (minimal_client.req.x_goal, minimal_client.req.y_goal, minimal_client.req.z_goal,minimal_client.req.time_of_move, minimal_client.req.type, response.confirmation))
                    return
    finally:
        minimal_client.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()