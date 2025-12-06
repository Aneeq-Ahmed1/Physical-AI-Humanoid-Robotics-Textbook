#!/usr/bin/env python3
"""
Basic ROS 2 service example for the Humanoid Robotics Textbook.

This example demonstrates how to create a service server and client
that communicate using a request/response pattern.
"""

import sys
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class MinimalService(Node):
    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f'Incoming request\na: {request.a} b: {request.b}')
        return response


class MinimalClient(Node):
    def __init__(self):
        super().__init__('minimal_client')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()


def run_service_server():
    """Run the service server"""
    rclpy.init()
    minimal_service = MinimalService()

    try:
        rclpy.spin(minimal_service)
    except KeyboardInterrupt:
        pass
    finally:
        minimal_service.destroy_node()
        rclpy.shutdown()


def run_service_client(a, b):
    """Run the service client with the given values"""
    rclpy.init()
    minimal_client = MinimalClient()

    try:
        response = minimal_client.send_request(int(a), int(b))
        minimal_client.get_logger().info(f'Result of add_two_ints: {response.sum}')
    except KeyboardInterrupt:
        pass
    finally:
        minimal_client.destroy_node()
        rclpy.shutdown()


def main(args=None):
    if len(sys.argv) == 1:
        # Run as server
        print("Running as service server. Use --client mode to run client.")
        run_service_server()
    elif len(sys.argv) >= 4 and sys.argv[1] == '--client':
        # Run as client
        a = sys.argv[2]
        b = sys.argv[3]
        run_service_client(a, b)
    else:
        print("Usage:")
        print("  To run as server: python3 service_example.py")
        print("  To run as client: python3 service_example.py --client <a> <b>")


if __name__ == '__main__':
    main()