# Data Model: Physical AI & Humanoid Robotics Textbook Project

This document outlines the key entities and their relationships as conceptualized for the "Physical AI & Humanoid Robotics Textbook Project." These entities represent the fundamental concepts and components discussed throughout the textbook.

## Key Entities

### Robot Model

*   **Description**: Representation of a physical humanoid robot in simulation. This entity encapsulates the robot's kinematics, dynamics, sensor configurations, and actuator properties.
*   **Attributes (Conceptual)**:
    *   `robot_name`: Unique identifier for the robot model.
    *   `urdf_path`: Path to the Unified Robot Description Format (URDF) file defining the robot's structure.
    *   `joints`: Collection of robotic joints with properties like limits, types, and current positions.
    *   `links`: Collection of rigid bodies (links) comprising the robot.
    *   `sensors`: Configuration of various sensors (e.g., cameras, lidar, IMU) attached to the robot, including their type, placement, and data output formats.
    *   `actuators`: Definition of motors or other actuation mechanisms for controlling robot movement.

### ROS 2 Node

*   **Description**: An independent executable processing unit in ROS 2. Nodes communicate with each other using topics, services, and actions. This entity represents the software components that perform specific tasks within the robot's control system.
*   **Attributes (Conceptual)**:
    *   `node_name`: Unique name for the ROS 2 node.
    *   `executables`: The code responsible for the node's logic.
    *   `topics_published`: List of ROS 2 topics this node publishes data to, including message types.
    *   `topics_subscribed`: List of ROS 2 topics this node subscribes to, including message types.
    *   `services_provided`: List of ROS 2 services this node offers.
    *   `services_used`: List of ROS 2 services this node calls.
    *   `parameters`: Configuration parameters for the node.

### Simulation Environment

*   **Description**: The virtual space where robot models are tested and behaviors are developed without relying on physical hardware. This includes platforms like Gazebo and Unity.
*   **Attributes (Conceptual)**:
    *   `environment_name`: Identifier for the simulation environment (e.g., "Gazebo", "Unity").
    *   `terrain_properties`: Characteristics of the simulated ground (friction, texture).
    *   `objects_present`: List of static and dynamic objects within the environment, including their models and positions.
    *   `physics_engine_config`: Configuration settings for the underlying physics engine (e.g., gravity, time steps, solvers).
    *   `rendering_settings`: Visual fidelity settings (e.g., lighting, shadows, textures).

### Perception Pipeline

*   **Description**: Components for processing sensor data to understand the environment. This typically involves processing visual data from cameras, depth sensors, and lidar to detect objects, map the environment, and track motion.
*   **Attributes (Conceptual)**:
    *   `pipeline_name`: Name of the perception pipeline.
    *   `sensor_inputs`: Types of sensors providing data (e.g., RGB camera, depth camera, lidar).
    *   `algorithms`: Machine learning models or classical algorithms used for processing (e.g., object detection, segmentation, SLAM).
    *   `outputs`: Types of information generated (e.g., object bounding boxes, semantic maps, pose estimates).
    *   `performance_metrics`: Latency, accuracy, processing throughput.

### Navigation Pipeline

*   **Description**: Components for path planning and movement control. This pipeline enables the robot to move from one point to another, avoiding obstacles, and reaching specified goals.
*   **Attributes (Conceptual)**:
    *   `pipeline_name`: Name of the navigation pipeline.
    *   `input_data`: Sensor data (e.g., lidar scans, camera images, odometry) and target goals.
    *   `localization_module`: Estimates the robot's position and orientation.
    *   `mapping_module`: Builds or updates an environmental map.
    *   `path_planner`: Generates a global and local path to the target.
    *   `controller`: Executes motor commands to follow the planned path.
    *   `obstacle_avoidance_system`: Handles dynamic obstacle detection and avoidance.

### Manipulation Pipeline

*   **Description**: Components for robotic arm/hand control for object interaction. This pipeline manages grasping, moving, and placing objects.
*   **Attributes (Conceptual)**:
    *   `pipeline_name`: Name of the manipulation pipeline.
    *   `target_object_data`: Information about the object to be manipulated (e.g., pose, geometry, type).
    *   `inverse_kinematics_solver`: Calculates joint angles required to reach a target pose.
    *   `trajectory_planner`: Generates smooth, collision-free arm movements.
    *   `gripper_controller`: Manages the opening and closing of the robot's end-effector.
    *   `force_feedback_system`: Uses force/torque sensors for compliant manipulation.

### LLM (Large Language Model)

*   **Description**: An AI model for natural language understanding and generation, used here for interpreting human commands and generating high-level task plans for the robot.
*   **Attributes (Conceptual)**:
    *   `model_name`: Identifier for the specific LLM being used.
    *   `input_modalities`: Text, speech (after ASR).
    *   `output_format`: Natural language responses, structured action plans (e.g., JSON, YAML).
    *   `context_window_size`: Amount of historical conversation/data the LLM can process.
    *   `fine_tuning_data`: Specific datasets used to adapt the LLM for robotics tasks.

### VLA (Vision-Language-Action)

*   **Description**: A framework integrating visual perception, language understanding, and robotic actions. This entity represents the overarching system that enables a robot to interpret multimodal commands and execute complex tasks.
*   **Attributes (Conceptual)**:
    *   `framework_name`: Identifier for the VLA framework.
    *   `vision_module`: Integration point for perception pipeline outputs.
    *   `language_module`: Integration point for LLM/ASR outputs.
    *   `action_module`: Integration point for manipulation/navigation pipelines.
    *   `multimodal_fusion_strategy`: How visual and language data are combined for reasoning.
    *   `task_planner`: Component responsible for breaking down high-level language commands into executable sub-tasks.
    *   `error_handling_mechanisms`: Strategies for dealing with interpretation errors or execution failures.
