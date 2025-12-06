# ROS 2 Architecture: Nodes, Topics, and Services

## Introduction

Understanding the fundamental communication patterns in ROS 2 is crucial for developing effective robotic applications. This section covers the three primary communication paradigms: Nodes (processes), Topics (publish/subscribe), and Services (request/response). These form the backbone of ROS 2's distributed computing architecture.

## Nodes: The Basic Computational Units

In ROS 2, a **node** is an executable that uses ROS 2 to communicate with other nodes. Nodes are the basic building blocks of a ROS 2 program, and they are organized into packages to form a complete ROS 2 application.

### Creating a Node

A node in ROS 2 is typically implemented as a class that inherits from `rclpy.Node` (in Python) or `rclcpp::Node` (in C++). Here's the basic structure:

```python
import rclpy
from rclpy.node import Node

class MinimalNode(Node):
    def __init__(self):
        super().__init__('minimal_node')
        # Node initialization code here

def main(args=None):
    rclpy.init(args=args)
    node = MinimalNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Node Characteristics

- Each node has a unique name within the ROS 2 graph
- Nodes can be started and stopped independently
- Nodes communicate with each other through topics, services, and actions
- Nodes can be written in different languages (Python, C++, etc.)

## Topics: Publish/Subscribe Communication

**Topics** enable asynchronous, one-to-many communication between nodes using a publish/subscribe pattern. This is ideal for streaming data like sensor readings, robot states, or control commands.

### Publisher-Subscriber Pattern

- **Publisher**: A node that sends data to a topic
- **Subscriber**: A node that receives data from a topic
- **Topic**: The named bus over which messages are sent

### Quality of Service (QoS) Settings

ROS 2 allows you to configure how messages are delivered using Quality of Service profiles:

- **Reliability**: Best effort vs. reliable delivery
- **Durability**: Volatile vs. transient local (for late-joining subscribers)
- **History**: Keep all messages vs. keep last N messages
- **Deadline**: Maximum time between consecutive messages

### Example: Publisher Implementation

You can find the complete publisher example in the code-examples/ros2-examples/publisher.py file:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'chatter', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello World: {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1


def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()

    try:
        rclpy.spin(minimal_publisher)
    except KeyboardInterrupt:
        pass
    finally:
        minimal_publisher.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

To run this publisher:
```bash
python3 code-examples/ros2-examples/publisher.py
```

### Example: Subscriber Implementation

You can find the complete subscriber example in the code-examples/ros2-examples/subscriber.py file:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'chatter',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()

    try:
        rclpy.spin(minimal_subscriber)
    except KeyboardInterrupt:
        pass
    finally:
        minimal_subscriber.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

To run this subscriber:
```bash
python3 code-examples/ros2-examples/subscriber.py
```

## Services: Request/Response Communication

**Services** provide synchronous, one-to-one communication between nodes using a request/response pattern. This is ideal for operations that require a specific response or acknowledgment.

### Service Characteristics

- **Service Client**: Sends a request and waits for a response
- **Service Server**: Receives requests and sends responses
- **Service Interface**: Defines the request and response message types

### Example: Service Definition (example_interfaces/srv/AddTwoInts.srv)

```
int64 a
int64 b
---
int64 sum
```

### Example: Service Implementation

You can find the complete service example (both server and client) in the code-examples/ros2-examples/service_example.py file:

```python
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
```

To run the service server:
```bash
python3 code-examples/ros2-examples/service_example.py
```

To run the service client:
```bash
python3 code-examples/ros2-examples/service_example.py --client 1 2
```

## Actions: Long-Running Tasks with Feedback

**Actions** are a more advanced communication pattern that supports long-running tasks with feedback, goal management, and cancellation. This is ideal for navigation, manipulation, or other tasks that take time to complete.

### Action Characteristics

- **Goal**: Request to start an action with specific parameters
- **Feedback**: Continuous updates on action progress
- **Result**: Final outcome when the action completes
- **Cancel**: Ability to cancel a running action

## Communication Patterns in Humanoid Robotics

### Sensor Data Distribution
- **Topics**: Camera images, LIDAR scans, IMU data, joint states
- **QoS**: Often requires reliable delivery with appropriate history settings

### Control Commands
- **Topics**: Velocity commands, joint position commands
- **QoS**: May require best-effort delivery for real-time control

### High-Level Commands
- **Services**: Set robot configuration, save map, calibrate sensors
- **Actions**: Navigate to pose, pick and place object, follow person

## Best Practices for ROS 2 Communication

### Topic Best Practices
- Use meaningful topic names following ROS naming conventions
- Consider QoS settings carefully based on application requirements
- Use appropriate message types (standard vs. custom)
- Implement proper error handling and node lifecycle management

### Service Best Practices
- Use services for operations that require a response
- Implement timeouts to prevent hanging requests
- Design service interfaces to be intuitive and efficient
- Consider whether actions might be more appropriate for long-running operations

### Performance Considerations
- Minimize message size to reduce network overhead
- Use appropriate serialization formats
- Consider message frequency and its impact on system performance
- Monitor network usage in distributed systems

## Tools for Understanding Communication

ROS 2 provides several tools to visualize and debug communication:

- `ros2 topic`: List, echo, publish, and info about topics
- `ros2 service`: List, call, and info about services
- `ros2 action`: List, send goals, and info about actions
- `rqt_graph`: Visualize the ROS 2 computation graph
- `ros2 bag`: Record and replay messages for analysis

## Summary

ROS 2's communication architecture provides flexible and robust mechanisms for distributed robotic applications. Understanding nodes, topics, services, and actions is fundamental to building effective humanoid robotic systems. The publish/subscribe model is ideal for sensor data and control commands, while services and actions provide synchronous communication and long-running task management respectively.

In the next sections, we'll implement practical examples of these communication patterns and integrate them into humanoid robotics applications.

## Acceptance Test Scenarios

### Test Scenario 1: Basic Publisher-Subscriber Communication
**Objective**: Verify that messages are correctly published and received between nodes.

**Steps**:
1. Launch the publisher node: `python3 code-examples/ros2-examples/publisher.py`
2. In a separate terminal, launch the subscriber node: `python3 code-examples/ros2-examples/subscriber.py`
3. Observe that the subscriber receives and displays messages from the publisher
4. Verify that message content is correctly transmitted (e.g., "Hello World: X" where X is incrementing)

**Expected Result**:
- Publisher sends messages at approximately 2Hz (every 0.5 seconds)
- Subscriber receives messages and logs them to the console
- Message sequence numbers increment correctly
- No errors or exceptions occur

### Test Scenario 2: Service Request-Response Communication
**Objective**: Verify that service requests are correctly processed and responses are returned.

**Steps**:
1. Launch the service server: `python3 code-examples/ros2-examples/service_example.py`
2. In a separate terminal, run the service client: `python3 code-examples/ros2-examples/service_example.py --client 5 3`
3. Verify that the service returns the correct sum (8 in this example)
4. Test with different values to ensure the service works correctly

**Expected Result**:
- Service server receives the request with parameters (5, 3)
- Service server processes the request and returns the sum (8)
- Service client receives and displays the correct result
- No errors or exceptions occur

### Test Scenario 3: Topic Communication Quality of Service
**Objective**: Verify that QoS settings affect communication behavior as expected.

**Steps**:
1. Modify the publisher and subscriber examples to use different QoS profiles (e.g., reliable vs. best effort)
2. Launch both nodes and observe communication behavior
3. Test with various QoS settings and document differences in behavior

**Expected Result**:
- Reliable QoS ensures all messages are delivered
- Best effort QoS may drop messages under high load but with lower latency
- Durability settings affect late-joining subscribers appropriately

### Test Scenario 4: Node Discovery and Communication
**Objective**: Verify that nodes can discover and communicate with each other on the ROS 2 network.

**Steps**:
1. Start the ROS 2 daemon: `ros2 daemon start`
2. Launch publisher and subscriber nodes
3. Use `ros2 node list` to verify both nodes are discovered
4. Use `ros2 topic list` to verify the topic is discovered
5. Use `ros2 topic info /chatter` to verify topic connection status

**Expected Result**:
- Both publisher and subscriber nodes appear in the node list
- The `/chatter` topic appears in the topic list
- Topic info shows active publisher and subscriber connections
- Nodes can communicate successfully

### Test Scenario 5: Error Handling and Graceful Shutdown
**Objective**: Verify that nodes handle errors and shutdown gracefully.

**Steps**:
1. Launch publisher and subscriber nodes
2. Terminate nodes using Ctrl+C
3. Verify that nodes cleanup resources properly
4. Check that no zombie processes remain

**Expected Result**:
- Nodes respond to SIGINT (Ctrl+C) and begin shutdown process
- Nodes properly destroy ROS 2 entities before exiting
- No resource leaks or zombie processes remain
- All logs indicate clean shutdown