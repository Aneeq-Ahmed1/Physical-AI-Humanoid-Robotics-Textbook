# Gazebo Fundamentals: Physics-Based Simulation for Humanoid Robots

## Introduction

Gazebo is a powerful, open-source robotics simulator that provides high-fidelity physics simulation, realistic sensor models, and a rich development environment. For humanoid robotics, Gazebo enables the testing and validation of complex locomotion, manipulation, and perception algorithms in a safe, controlled environment.

This section covers the essential concepts and techniques for using Gazebo effectively in humanoid robotics applications.

## Gazebo Architecture and Components

### Core Components

#### Physics Engine
Gazebo supports multiple physics engines:
- **ODE (Open Dynamics Engine)**: Default engine, good for general-purpose simulation
- **Bullet**: Fast and robust, suitable for complex contact scenarios
- **Simbody**: Multi-body dynamics engine, good for biomechanical simulations
- **DART**: Dynamic Animation and Robotics Toolkit, advanced contact handling

#### Rendering Engine
- **OGRE**: 3D rendering engine for visualization
- **OpenGL**: Hardware-accelerated graphics rendering
- **GUI**: Interactive user interface for simulation control

#### Sensor Simulation
Gazebo provides realistic simulation of various sensors:
- Cameras (RGB, depth, stereo)
- LIDAR and 2D/3D laser scanners
- IMU sensors
- Force/torque sensors
- GPS and magnetometer
- Joint position, velocity, and effort sensors

### Gazebo Simulation Pipeline

1. **Model Loading**: Robot and environment models are loaded
2. **Physics Update**: Physics engine calculates forces and movements
3. **Sensor Update**: Simulated sensors generate data based on the current state
4. **Rendering**: Visualization is updated for the GUI
5. **Communication**: Data is published to ROS topics or other interfaces

## Setting Up Gazebo for Humanoid Robotics

### Installation

Gazebo can be installed as part of the ROS ecosystem:

```bash
# Install Gazebo with ROS 2
sudo apt update
sudo apt install ros-humble-gazebo-ros-pkgs ros-humble-gazebo-plugins

# Or install standalone Gazebo Garden
sudo apt install gazebo-garden
```

### Basic Launch

To launch Gazebo with a simple empty world:

```bash
# Using ROS 2 launch
ros2 launch gazebo_ros empty_world.launch.py

# Or standalone
gazebo
```

## Robot Modeling with URDF and SDF

### URDF vs. SDF

**URDF (Unified Robot Description Format)** is used primarily in ROS and describes robot kinematics and visual properties:

```xml
<?xml version="1.0"?>
<robot name="simple_humanoid">
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.2 0.1 0.1"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="0.2 0.1 0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01"/>
    </inertial>
  </link>
</robot>
```

**SDF (Simulation Description Format)** is Gazebo's native format and includes physics and simulation-specific properties:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <model name="simple_humanoid">
    <link name="base_link">
      <pose>0 0 0.1 0 0 0</pose>
      <visual name="visual">
        <geometry>
          <box>
            <size>0.2 0.1 0.1</size>
          </box>
        </geometry>
      </visual>
      <collision name="collision">
        <geometry>
          <box>
            <size>0.2 0.1 0.1</size>
          </box>
        </geometry>
      </collision>
      <inertial>
        <mass>1.0</mass>
        <inertia>
          <ixx>0.01</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.01</iyy>
          <iyz>0.0</iyz>
          <izz>0.01</izz>
        </inertia>
      </inertial>
    </link>
  </model>
</sdf>
```

### Key Considerations for Humanoid Robots

#### Mass Distribution
- Accurate mass properties are crucial for stable locomotion
- Use CAD software to calculate mass properties when possible
- Consider the impact of payloads and accessories

#### Joint Limits and Dynamics
- Set realistic joint limits based on physical constraints
- Configure damping and friction to match real-world behavior
- Use appropriate gear ratios and motor characteristics

#### Contact Modeling
- Configure contact stiffness and damping for stable contact
- Use appropriate friction coefficients for different materials
- Consider the impact of foot geometry on walking stability

## Gazebo Plugins for Humanoid Robots

### ROS 2 Control Integration

The `gazebo_ros_control` plugin allows integration with ROS 2 control framework:

```xml
<gazebo>
  <plugin name="gazebo_ros_control" filename="libgazebo_ros_control.so">
    <parameters>$(find my_robot_description)/config/my_robot_controllers.yaml</parameters>
  </plugin>
</gazebo>
```

### Sensor Plugins

Gazebo provides various sensor plugins that can be integrated into URDF:

```xml
<gazebo reference="camera_link">
  <sensor name="camera" type="camera">
    <update_rate>30</update_rate>
    <camera name="head">
      <horizontal_fov>1.3962634</horizontal_fov>
      <image>
        <width>800</width>
        <height>600</height>
        <format>R8G8B8</format>
      </image>
      <clip>
        <near>0.1</near>
        <far>100</far>
      </clip>
    </camera>
    <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
      <frame_name>camera_optical_frame</frame_name>
      <topic_name>image_raw</topic_name>
    </plugin>
  </sensor>
</gazebo>
```

### Physics Plugins

For humanoid robots, you might need custom physics plugins for:

- Custom contact processing
- External force application
- Specialized control algorithms
- Integration with external simulators

## Creating Humanoid Robot Models

### Basic Humanoid Structure

A humanoid robot typically includes:

- **Torso**: Main body with sensors and computing
- **Head**: With cameras, microphones, and displays
- **Arms**: With shoulders, elbows, wrists, and hands
- **Legs**: With hips, knees, ankles, and feet
- **Joints**: With appropriate ranges of motion

### Example Humanoid Configuration

For a complete example of a humanoid robot model, see the `code-examples/gazebo-unity-examples/humanoid.urdf` file which contains a detailed 18-DOF humanoid model with:

- Torso and head with appropriate mass properties
- Two legs with hip, knee, and ankle joints
- Two arms with shoulder, elbow, and wrist joints
- Proper inertial properties for stable simulation
- Gazebo plugin configuration for ROS control

Here's an excerpt showing the main torso and head definition:

```xml
<?xml version="1.0"?>
<robot name="simple_humanoid">

  <!-- Base/Pelvis Link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.2 0.25 0.3"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.2 0.25 0.3"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10.0"/>
      <inertia ixx="0.2" ixy="0.0" ixz="0.0" iyy="0.2" iyz="0.0" izz="0.2"/>
    </inertial>
  </link>

  <!-- Torso -->
  <joint name="pelvis_torso_joint" type="fixed">
    <parent link="base_link"/>
    <child link="torso"/>
    <origin xyz="0.0 0.0 0.25" rpy="0 0 0"/>
  </joint>

  <link name="torso">
    <visual>
      <geometry>
        <box size="0.25 0.25 0.4"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.25 0.25 0.4"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="8.0"/>
      <inertia ixx="0.2" ixy="0.0" ixz="0.0" iyy="0.2" iyz="0.0" izz="0.2"/>
    </inertial>
  </link>

  <!-- Head -->
  <joint name="torso_head_joint" type="fixed">
    <parent link="torso"/>
    <child link="head"/>
    <origin xyz="0.0 0.0 0.35" rpy="0 0 0"/>
  </joint>

  <link name="head">
    <visual>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="2.0"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01"/>
    </inertial>
  </link>

  <!-- Additional joints and links for complete humanoid continue in the full file... -->
</robot>
```

To launch this humanoid robot in Gazebo, use the launch file provided in `code-examples/gazebo-unity-examples/launch/humanoid_sim.launch.py`:

```python
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Package and file paths
    pkg_gazebo_ros = FindPackageShare('gazebo_ros')

    # Launch configuration variables
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_rviz = LaunchConfiguration('use_rviz')

    # Declare launch arguments
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )

    # Start Gazebo server
    start_gazebo_server_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={
            'world': os.path.join(
                FindPackageShare('gazebo_unity_examples').find('gazebo_unity_examples'),
                'worlds',
                'empty.world'
            ),
            'verbose': 'true',
            'pause': 'false'
        }.items()
    )

    # Robot State Publisher node
    robot_state_publisher_cmd = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'robot_description': get_robot_description(  # This function reads the URDF
                PathJoinSubstitution([FindPackageShare('gazebo_unity_examples'), 'urdf', 'humanoid.urdf'])
            )
        }]
    )

    # ... (additional nodes and configuration)

    ld = LaunchDescription()
    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(start_gazebo_server_cmd)
    ld.add_action(robot_state_publisher_cmd)
    # ... (additional actions)

    return ld

def get_robot_description(urdf_path):
    """Read the URDF file and return its content as a string."""
    with open(urdf_path, 'r') as infp:
        robot_desc = infp.read()
    return {'robot_description': robot_desc}
```

To run the simulation:

```bash
# Launch the humanoid robot in Gazebo
ros2 launch gazebo_unity_examples humanoid_sim.launch.py
```

## Simulation Scenarios for Humanoid Robots

### Locomotion Testing
- Walking on flat ground
- Stair climbing
- Obstacle navigation
- Balance recovery from disturbances

### Manipulation Tasks
- Object grasping and manipulation
- Tool usage
- Bimanual coordination
- Human-robot interaction scenarios

### Perception Challenges
- Object recognition in cluttered environments
- Human pose estimation
- Dynamic scene understanding
- Multi-modal sensor fusion

## Performance Optimization

### Simulation Speed
- Adjust physics engine parameters for desired speed
- Reduce model complexity where appropriate
- Use simplified collision models for non-critical components
- Optimize sensor update rates

### Stability Considerations
- Proper time step selection
- Appropriate contact parameters
- Adequate joint damping
- Realistic actuator dynamics

## Debugging and Visualization

### Gazebo GUI Tools
- Model and joint visualization
- Force and torque display
- Sensor data visualization
- Physics properties inspection

### Common Issues and Solutions
- Jittering joints: Adjust damping or increase physics update rate
- Penetrating objects: Increase contact stiffness or adjust time step
- Unstable walking: Verify mass properties and contact parameters
- Slow simulation: Simplify models or adjust physics parameters

## Integration with ROS 2

### Launch Files

Example launch file for humanoid simulation:

```python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Launch configuration variables
    model = LaunchConfiguration('model')
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Declare launch arguments
    declare_model_path = DeclareLaunchArgument(
        name='model',
        default_value='path/to/humanoid.urdf',
        description='Absolute path to robot urdf file'
    )

    declare_use_sim_time = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )

    # Start Gazebo server
    start_gazebo_server_cmd = Node(
        package='gazebo_ros',
        executable='gzserver',
        parameters=[{'use_sim_time': use_sim_time}],
        arguments=['-s', 'libgazebo_ros_init.so',
                   '-s', 'libgazebo_ros_factory.so'],
        output='screen'
    )

    # Start Gazebo client
    start_gazebo_client_cmd = Node(
        package='gazebo_ros',
        executable='gzclient',
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    # Robot State Publisher
    robot_state_publisher_cmd = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'use_sim_time': use_sim_time,
                    'robot_description': model}],
        output='screen'
    )

    # Spawn robot in Gazebo
    spawn_entity_cmd = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'humanoid_robot',
                   '-topic', 'robot_description'],
        output='screen'
    )

    # Create launch description
    ld = LaunchDescription()

    # Add actions to launch description
    ld.add_action(declare_model_path)
    ld.add_action(declare_use_sim_time)
    ld.add_action(start_gazebo_server_cmd)
    ld.add_action(start_gazebo_client_cmd)
    ld.add_action(robot_state_publisher_cmd)
    ld.add_action(spawn_entity_cmd)

    return ld
```

## Best Practices

### Model Development
- Start with simple models and gradually increase complexity
- Validate each component before integration
- Use consistent units throughout the model
- Document assumptions and limitations

### Simulation Design
- Create reproducible simulation conditions
- Log simulation parameters for result validation
- Use realistic noise models for sensors
- Validate simulation results against physical robots when possible

### Performance
- Profile simulation performance regularly
- Balance accuracy with computational requirements
- Use appropriate model simplifications
- Consider parallel simulation for testing

## Summary

Gazebo provides a powerful platform for humanoid robotics simulation, offering physics-based simulation, sensor modeling, and integration with ROS 2. Proper configuration of robot models, physics parameters, and simulation scenarios is essential for effective humanoid robot development and testing.

In the next sections, we'll explore Unity for high-fidelity visual simulation and how to integrate both platforms for comprehensive humanoid robotics development.