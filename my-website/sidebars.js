// @ts-check

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.

 @type {import('@docusaurus/plugin-content-docs').SidebarsConfig}
 */
const sidebars = {
  // Main textbook sidebar
  textbookSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Chapter 01: ROS 2 - The Robotic Nervous System',
      items: [
        'ros2/index',
        'ros2/nodes-topics-services',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 02: Simulate Humanoid Robots',
      items: [
        'simulation/index',
        'simulation/gazebo-fundamentals',
        'simulation/unity-robotics',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 03: NVIDIA Isaac - AI-Robot Brain',
      items: [
        'nvidia-isaac/index',
        'nvidia-isaac/perception-pipelines',
        'nvidia-isaac/navigation-manipulation',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 04: VLA and LLM Integration',
      items: [
        'vla-llm/index',
        'vla-llm/whisper-integration',
        'vla-llm/llm-task-planning',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 05: Capstone Project - Autonomous Humanoid',
      items: [
        'capstone-project/index',
        'capstone-project/system-integration-guide',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 06: Human-Robot Interaction Design',
      items: [
        'human-robot-interaction-design/index',
        'human-robot-interaction-design/ethical-considerations',
      ],
    },
  ],
};

export default sidebars;
