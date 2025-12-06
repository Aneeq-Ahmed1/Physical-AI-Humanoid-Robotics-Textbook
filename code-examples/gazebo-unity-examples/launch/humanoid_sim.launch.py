import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Package and file paths
    pkg_gazebo_ros = FindPackageShare('gazebo_ros')
    pkg_gazebo_unity_examples = FindPackageShare('gazebo_unity_examples')  # This would be your package

    # File paths
    world_file = PathJoinSubstitution([pkg_gazebo_unity_examples, 'worlds', 'simple_humanoid.world'])
    robot_description_path = PathJoinSubstitution([pkg_gazebo_unity_examples, 'urdf', 'humanoid.urdf'])

    # Launch configuration variables
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_rviz = LaunchConfiguration('use_rviz')
    world = LaunchConfiguration('world')
    robot_name = LaunchConfiguration('robot_name')
    robot_namespace = LaunchConfiguration('robot_namespace')

    # Declare launch arguments
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )

    declare_use_rviz_cmd = DeclareLaunchArgument(
        name='use_rviz',
        default_value='true',
        description='Whether to start RViz'
    )

    declare_world_cmd = DeclareLaunchArgument(
        name='world',
        default_value='empty',
        description='Choose one of the world files from `/gazebo_unity_examples/worlds` directory'
    )

    declare_robot_name_cmd = DeclareLaunchArgument(
        name='robot_name',
        default_value='humanoid_robot',
        description='Name of the robot'
    )

    declare_robot_namespace_cmd = DeclareLaunchArgument(
        name='robot_namespace',
        default_value='',
        description='Namespace for the robot'
    )

    # Specify the world file to use
    world_path = os.path.join(
        FindPackageShare('gazebo_unity_examples').find('gazebo_unity_examples'),
        'worlds',
        'empty.world'
    )

    # Start Gazebo server
    start_gazebo_server_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={
            'world': world_path,
            'verbose': 'true',
            'pause': 'false'
        }.items()
    )

    # Start Gazebo client
    start_gazebo_client_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
        ),
        condition=IfCondition(use_rviz)
    )

    # Robot State Publisher node
    robot_state_publisher_cmd = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        namespace=robot_namespace,
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'robot_description': get_robot_description(robot_description_path)
        }]
    )

    # Joint State Publisher node (for visualization)
    joint_state_publisher_cmd = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        namespace=robot_namespace,
        parameters=[{
            'use_sim_time': use_sim_time,
            'rate': 50.0,
            'source_list': ['joint_states']
        }]
    )

    # Spawn the robot in Gazebo
    spawn_robot_cmd = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', robot_name,
            '-topic', [robot_namespace, '/robot_description'].join('') if robot_namespace else '/robot_description',
            '-x', '0', '-y', '0', '-z', '1.0'  # Spawn the robot 1m above ground
        ],
        output='screen'
    )

    # RViz node
    rviz_cmd = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=[
            '-d', os.path.join(
                FindPackageShare('gazebo_unity_examples').find('gazebo_unity_examples'),
                'rviz',
                'humanoid_view.rviz'
            )
        ],
        condition=IfCondition(use_rviz),
        parameters=[{'use_sim_time': use_sim_time}]
    )

    # Create the launch description and populate
    ld = LaunchDescription()

    # Declare the launch options
    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(declare_use_rviz_cmd)
    ld.add_action(declare_world_cmd)
    ld.add_action(declare_robot_name_cmd)
    ld.add_action(declare_robot_namespace_cmd)

    # Add any actions to launch description
    ld.add_action(start_gazebo_server_cmd)
    ld.add_action(start_gazebo_client_cmd)
    ld.add_action(robot_state_publisher_cmd)
    ld.add_action(joint_state_publisher_cmd)
    ld.add_action(spawn_robot_cmd)
    ld.add_action(rviz_cmd)

    return ld


def get_robot_description(urdf_path):
    """Read the URDF file and return its content as a string."""
    with open(urdf_path, 'r') as infp:
        robot_desc = infp.read()
    return {'robot_description': robot_desc}