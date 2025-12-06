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

    void HandleAnimation()
    {
        if (animator != null)
        {
            // Update animation parameters based on movement
            float speed = new Vector3(rb.velocity.x, 0, rb.velocity.z).magnitude;
            animator.SetFloat("Speed", speed);
            animator.SetFloat("Direction", Input.GetAxis("Horizontal"));
        }
    }

    void ProcessROSCommands()
    {
        // This would handle commands received from ROS
        // For example: joint angles, movement commands, etc.
    }

    void InitializeROSConnection()
    {
        // Initialize ROS TCP connector
        // This would typically use ROS# or similar Unity-ROS bridge
    }

    void OnCollisionEnter(Collision collision)
    {
        // Check if the humanoid has landed on the ground
        foreach (ContactPoint contact in collision.contacts)
        {
            if (contact.normal.y > 0.5f) // If contact normal is mostly upward
            {
                isGrounded = true;
                break;
            }
        }
    }

    void OnCollisionExit(Collision collision)
    {
        // Check if the humanoid has left the ground
        isGrounded = false;
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

    private ConfigurableJoint FindJointByName(string name)
    {
        foreach (ConfigurableJoint joint in jointControllers)
        {
            if (joint.name == name || joint.gameObject.name == name)
            {
                return joint;
            }
        }
        return null;
    }

    // Visualization for debugging
    void OnDrawGizmosSelected()
    {
        if (jointControllers != null)
        {
            foreach (ConfigurableJoint joint in jointControllers)
            {
                if (joint != null)
                {
                    Gizmos.color = Color.red;
                    Gizmos.DrawWireSphere(joint.transform.position, 0.05f);
                }
            }
        }
    }
}