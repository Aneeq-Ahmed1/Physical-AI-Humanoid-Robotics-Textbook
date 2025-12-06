# Unity Robotics: High-Fidelity Visual Simulation

## Introduction

Unity is a powerful, cross-platform game engine that has emerged as a leading platform for high-fidelity visual simulation in robotics. Unlike Gazebo's focus on physics simulation, Unity excels at creating photorealistic environments and visual content, making it ideal for computer vision training, virtual reality interfaces, and human-robot interaction studies.

Unity's robotics applications include:
- Photorealistic sensor simulation for computer vision
- Virtual and augmented reality interfaces
- Reinforcement learning environments
- Human-robot interaction studies
- Training data generation for perception systems

## Unity Robotics Hub and Packages

### Unity Robotics Hub

Unity Robotics Hub is a centralized package manager for robotics-related tools and packages:

- **Unity Robot Toolkit (URT)**: Framework for robotics simulation
- **Unity Perception Package**: Tools for generating labeled synthetic data
- **Unity ML-Agents**: Platform for reinforcement learning
- **ROS#**: ROS bridge for Unity
- **Unity Simulation**: Tools for large-scale simulation

### Key Robotics Packages

#### Unity Perception Package
- Synthetic data generation with ground truth annotations
- Domain randomization for robust perception
- 2D and 3D bounding box annotations
- Semantic segmentation masks
- Depth and normal maps
- Point cloud generation

#### ML-Agents Toolkit
- Reinforcement learning framework
- Imitation learning capabilities
- Multi-agent environments
- Curriculum learning support
- Cross-platform deployment

## Setting Up Unity for Robotics

### Installation

1. Download Unity Hub from the Unity website
2. Install Unity Editor (recommended version 2021.3 LTS or newer)
3. Install required packages via Package Manager:
   - Unity Perception
   - ML-Agents
   - XR packages (if needed for VR/AR)

### Unity ROS Bridge (ROS#)

The ROS# package enables communication between Unity and ROS/ROS 2:

```csharp
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Sensor;

public class CameraPublisher : MonoBehaviour
{
    ROSConnection ros;
    string topicName = "/unity_camera/image_raw";

    // Start is called before the first frame update
    void Start()
    {
        ros = ROSConnection.instance;
    }

    void OnRenderImage(RenderTexture source, RenderTexture destination)
    {
        // Capture image and send to ROS
        Texture2D image = new Texture2D(source.width, source.height);
        RenderTexture.active = source;
        image.ReadPixels(new Rect(0, 0, source.width, source.height), 0, 0);
        image.Apply();

        // Convert to ROS message and publish
        sensor_msgs.Image unityImage = ImageConversion.GetRenderTextureSensorMsg(source);
        ros.Send(topicName, unityImage);

        Graphics.Blit(source, destination);
    }
}
```

## Creating Humanoid Robot Models in Unity

### Importing Robot Models

Unity can import robot models in several formats:
- **URDF**: Using the Unity URDF Importer package
- **FBX/GLTF**: Standard 3D model formats
- **SDF**: With appropriate conversion tools

#### Using URDF Importer

1. Install the Unity URDF Importer package
2. Import your URDF file and associated meshes
3. Configure joint limits and dynamics
4. Set up collision detection

### Robot Control in Unity

For a complete example of humanoid robot control in Unity, see the `code-examples/gazebo-unity-examples/unity_project/Assets/Scripts/HumanoidController.cs` file, which implements:

- Joint control with target angle setting
- Movement input handling
- Animation parameter updates
- ROS connection management
- Ground contact detection

Here's an excerpt showing the main control structure:

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HumanoidController : MonoBehaviour
{
    [Header("Joint Configuration")]
    public List<ConfigurableJoint> jointControllers = new List<ConfigurableJoint>();

    [Header("Movement Parameters")]
    public float walkSpeed = 2.0f;
    public float turnSpeed = 50.0f;
    public float jumpForce = 5.0f;

    [Header("ROS Connection")]
    public bool useROSConnection = false;

    private Rigidbody rb;
    private Animator animator;
    private bool isGrounded = true;

    void Start()
    {
        rb = GetComponent<Rigidbody>();
        animator = GetComponent<Animator>();

        if (useROSConnection)
        {
            // Initialize ROS connection
            InitializeROSConnection();
        }
    }

    void Update()
    {
        HandleMovementInput();
        HandleAnimation();
    }

    void FixedUpdate()
    {
        if (useROSConnection)
        {
            // Handle ROS commands
            ProcessROSCommands();
        }
    }

    void HandleMovementInput()
    {
        if (useROSConnection)
            return; // Movement controlled by ROS

        float horizontal = Input.GetAxis("Horizontal");
        float vertical = Input.GetAxis("Vertical");

        // Basic movement
        Vector3 movement = new Vector3(horizontal, 0, vertical) * walkSpeed * Time.deltaTime;
        transform.Translate(movement, Space.World);

        // Turning
        if (horizontal != 0)
        {
            transform.Rotate(Vector3.up, horizontal * turnSpeed * Time.deltaTime);
        }

        // Jumping
        if (Input.GetKeyDown(KeyCode.Space) && isGrounded)
        {
            rb.AddForce(Vector3.up * jumpForce, ForceMode.Impulse);
            isGrounded = false;
        }
    }

    // Public methods for external control (e.g., from ROS)
    public void SetJointTarget(string jointName, float targetAngle)
    {
        ConfigurableJoint joint = FindJointByName(jointName);
        if (joint != null)
        {
            // Set the target rotation for the joint
            joint.targetRotation = Quaternion.Euler(0, 0, targetAngle);
        }
    }

    public void SetJointTargets(Dictionary<string, float> jointTargets)
    {
        foreach (var target in jointTargets)
        {
            SetJointTarget(target.Key, target.Value);
        }
    }
}
```

The Unity scene containing the humanoid robot is located at `code-examples/gazebo-unity-examples/unity_project/Assets/Scenes/HumanoidScene.unity`, which includes:

- Main camera setup for visualization
- Directional light for illumination
- Humanoid robot GameObject with proper components
- Physics configuration for realistic simulation

## Physics Simulation in Unity

### Unity Physics vs. Robotics-Specific Physics

Unity uses PhysX for physics simulation, which differs from robotics-focused engines like ODE or Bullet:

- **PhysX**: Optimized for visual fidelity and game performance
- **ODE/Bullet**: Optimized for stability and accuracy in robotic applications
- **Trade-offs**: Visual quality vs. physical accuracy

### Configuring Physics for Robotics

```csharp
using UnityEngine;

public class PhysicsConfig : MonoBehaviour
{
    void Start()
    {
        // Configure physics settings for robotics
        Physics.defaultSolverIterations = 10; // Increase for stability
        Physics.defaultSolverVelocityIterations = 2; // Increase for accuracy
        Physics.sleepThreshold = 0.001f; // Lower threshold for sensitive objects
        Physics.defaultContactOffset = 0.01f; // Contact offset for stable contacts
    }
}
```

### Contact Detection and Force Sensing

```csharp
using UnityEngine;

public class ForceSensor : MonoBehaviour
{
    public float forceThreshold = 1f;
    public bool isContactDetected = false;
    private Rigidbody rb;

    void Start()
    {
        rb = GetComponent<Rigidbody>();
    }

    void OnCollisionEnter(Collision collision)
    {
        float force = collision.impulse.magnitude / Time.fixedDeltaTime;
        if (force > forceThreshold)
        {
            isContactDetected = true;
            Debug.Log($"Contact detected with force: {force}");
            // Publish force data to ROS
        }
    }

    void OnCollisionExit(Collision collision)
    {
        isContactDetected = false;
    }
}
```

## Sensor Simulation in Unity

### Camera Simulation

Unity's cameras can simulate various sensor types:

```csharp
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Sensor;

public class CameraSensor : MonoBehaviour
{
    public Camera unityCamera;
    public string topicName = "/camera/rgb/image_raw";
    public int imageWidth = 640;
    public int imageHeight = 480;

    private ROSConnection ros;
    private RenderTexture renderTexture;

    void Start()
    {
        ros = ROSConnection.instance;

        // Create render texture for camera
        renderTexture = new RenderTexture(imageWidth, imageHeight, 24);
        unityCamera.targetTexture = renderTexture;
    }

    void Update()
    {
        // Capture image periodically
        if (Time.frameCount % 30 == 0) // 30 FPS
        {
            RenderTexture.active = renderTexture;
            Texture2D image = new Texture2D(imageWidth, imageHeight, TextureFormat.RGB24, false);
            image.ReadPixels(new Rect(0, 0, imageWidth, imageHeight), 0, 0);
            image.Apply();

            // Convert to byte array and publish
            byte[] imageData = image.EncodeToPNG();
            // Publish to ROS topic
        }
    }
}
```

### Depth and Semantic Segmentation

Unity's rendering pipeline can generate depth maps and semantic segmentation:

```csharp
using UnityEngine;

public class DepthSensor : MonoBehaviour
{
    public Camera depthCamera;
    public Shader depthShader;
    private RenderTexture depthTexture;

    void Start()
    {
        depthTexture = new RenderTexture(640, 480, 24, RenderTextureFormat.RFloat);
        depthCamera.targetTexture = depthTexture;
        depthCamera.SetReplacementShader(depthShader, "RenderType");
    }

    public float[] GetDepthData()
    {
        RenderTexture.active = depthTexture;
        Texture2D depthTex = new Texture2D(640, 480, TextureFormat.RFloat, false);
        depthTex.ReadPixels(new Rect(0, 0, 640, 480), 0, 0);
        depthTex.Apply();

        Color[] colors = depthTex.GetPixels();
        float[] depths = new float[colors.Length];

        for (int i = 0; i < colors.Length; i++)
        {
            depths[i] = colors[i].r; // Depth value is in the red channel
        }

        return depths;
    }
}
```

## Unity Perception for Synthetic Data

### Domain Randomization

Domain randomization helps create robust perception systems:

```csharp
using UnityEngine;
using Unity.Perception.Randomization.Samplers;
using Unity.Perception.Randomization.Parameters;

public class EnvironmentRandomizer : MonoBehaviour
{
    [Tooltip("The list of materials that can be assigned to the ground plane")]
    public MaterialList groundMaterials;

    [Tooltip("The range of possible ground plane rotations")]
    public RotationParameter groundRotation;

    [Tooltip("The range of possible lighting intensities")]
    public FloatParameter lightIntensity;

    void Start()
    {
        // Randomize environment at the start of each episode
        RandomizeEnvironment();
    }

    public void RandomizeEnvironment()
    {
        // Randomize ground material
        int materialIndex = Random.Range(0, groundMaterials.Count);
        // Apply material to ground plane

        // Randomize lighting
        float intensity = lightIntensity.Sample();
        // Apply intensity to lights in scene

        // Randomize object positions, colors, textures, etc.
    }
}
```

### Annotation Generation

Unity Perception can automatically generate annotations:

- **Bounding Boxes**: 2D and 3D bounding boxes for objects
- **Semantic Segmentation**: Pixel-level object classification
- **Instance Segmentation**: Individual object identification
- **Keypoint Annotation**: Joint positions for articulated objects
- **Depth Maps**: Per-pixel depth information

## ML-Agents for Robot Learning

### Setting Up ML-Agents

ML-Agents enables reinforcement learning in Unity:

1. Install ML-Agents package in Unity
2. Add Brain component to agents
3. Define observation space and actions
4. Train models using Python API

### Example: Balance Training for Humanoid Robot

```csharp
using Unity.MLAgents;
using Unity.MLAgents.Sensors;
using Unity.MLAgents.Actuators;

public class HumanoidBalanceAgent : Agent
{
    public Transform target;
    public float maxStep = 1000f;
    private int stepCount = 0;

    public override void OnEpisodeBegin()
    {
        // Reset robot position and target
        stepCount = 0;
        transform.position = new Vector3(0, 1, 0);
        transform.rotation = Quaternion.identity;
    }

    public override void CollectObservations(VectorSensor sensor)
    {
        // Observe robot state
        sensor.AddObservation(transform.position);
        sensor.AddObservation(transform.rotation);
        sensor.AddObservation(target.position);

        // Add joint angles, velocities, etc.
    }

    public override void OnActionReceived(ActionBuffers actions)
    {
        // Apply actions to joints
        float[] continuousActions = actions.ContinuousActions;

        // Map actions to joint torques or positions
        ApplyActionsToJoints(continuousActions);

        // Calculate reward
        float distanceToTarget = Vector3.Distance(transform.position, target.position);
        SetReward(1.0f - distanceToTarget / maxStep);

        stepCount++;
        if (stepCount > maxStep)
        {
            EndEpisode();
        }
    }

    private void ApplyActionsToJoints(float[] actions)
    {
        // Apply actions to robot joints
        // Implementation depends on robot structure
    }

    private void FixedUpdate()
    {
        // Check for termination conditions
        if (transform.position.y < 0.5f) // Fallen
        {
            SetReward(-1.0f);
            EndEpisode();
        }
    }
}
```

## Integration with ROS/ROS 2

### Communication Patterns

Unity can communicate with ROS/ROS 2 systems through:

#### TCP/IP Bridge (ROS#)
- Direct message passing between Unity and ROS nodes
- Support for standard ROS message types
- Real-time communication capabilities

#### Shared Memory
- Faster communication for high-frequency data
- Requires careful synchronization
- Platform-specific implementation

#### File-based Exchange
- For batch processing and offline analysis
- Synchronization mechanisms required
- Useful for training data generation

### Example ROS Integration

```csharp
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Std;
using RosMessageTypes.Geometry;

public class UnityROSBridge : MonoBehaviour
{
    ROSConnection ros;

    void Start()
    {
        ros = ROSConnection.instance;

        // Subscribe to ROS topics
        ros.Subscribe<UInt8MultiArrayMsg>("/unity/control", ControlCallback);
    }

    void ControlCallback(UInt8MultiArrayMsg controlMsg)
    {
        // Process control commands from ROS
        ProcessControlCommands(controlMsg.data);
    }

    void SendSensorData()
    {
        // Create and send sensor data to ROS
        JointStateMsg jointState = new JointStateMsg();
        // Populate joint state data
        ros.Send("/unity/joint_states", jointState);
    }
}
```

## Virtual and Augmented Reality Integration

### VR for Teleoperation

Unity enables VR interfaces for robot teleoperation:

- Immersive visualization of robot environment
- Intuitive control interfaces
- Real-time feedback and monitoring
- Multi-robot coordination interfaces

### AR for Human-Robot Collaboration

Augmented reality can enhance human-robot collaboration:

- Overlay robot intentions and plans
- Visualize robot sensor data
- Guide human operators
- Provide safety warnings

## Performance Optimization

### Rendering Optimization

For real-time robotics applications:

- Use Level of Detail (LOD) systems
- Optimize draw calls and batching
- Use occlusion culling
- Implement texture streaming

### Simulation Performance

- Optimize physics calculations
- Use fixed timestep for determinism
- Reduce unnecessary object updates
- Implement efficient sensor simulation

## Best Practices for Robotics Simulation

### Model Quality
- Balance visual fidelity with performance
- Use appropriate polygon counts
- Implement proper material properties
- Validate models against real-world counterparts

### Data Generation
- Use domain randomization appropriately
- Ensure data diversity for robust models
- Validate synthetic data quality
- Maintain consistency between simulation and reality

### Integration
- Design modular, reusable components
- Implement proper error handling
- Ensure determinism for reproducible results
- Validate communication protocols

## Troubleshooting Common Issues

### Physics Instability
- Increase solver iterations
- Adjust time step settings
- Verify mass and inertia properties
- Check joint configurations

### Performance Problems
- Profile rendering and physics separately
- Identify bottlenecks in sensor simulation
- Optimize material and shader complexity
- Consider level of detail systems

### Communication Issues
- Verify network connectivity
- Check message format compatibility
- Validate data serialization
- Monitor communication bandwidth

## Summary

Unity provides powerful capabilities for high-fidelity visual simulation in robotics, particularly for computer vision, perception training, and human-robot interaction studies. When combined with physics-based simulators like Gazebo, Unity enables comprehensive simulation environments for humanoid robotics development.

The integration of Unity with ROS/ROS 2, ML-Agents, and Perception packages creates a complete ecosystem for robotics research and development, from perception and learning to human interaction and deployment.