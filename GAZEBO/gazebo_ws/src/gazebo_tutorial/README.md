# 🌍 Gazebo Simulation — `gazebo_tutorial`

![Gazebo](https://img.shields.io/badge/Simulator-Gazebo_Harmonic-orange)
![SDF](https://img.shields.io/badge/Format-SDF-lightgrey)
![ROS_2](https://img.shields.io/badge/Integration-ROS_2_Jazzy-blue?logo=ros)

Simulation experiments using **Gazebo Harmonic** integrated with ROS 2 Jazzy. The core deliverable is a manually written SDF robot model (Four-Wheel-Steering robot), covering all mechanical and sensor definitions from scratch.

## 🏗️ Project Structure

gazebo_ws/src/gazebo_tutorial/
├── buidling_robot.sdf # Hand-written SDF robot model
└── fws_robot_harmonic.zip # Complete FWS robot Gazebo package

text

## 🎯 Key Implementations

- **SDF Modeling from Scratch:** Defined robot geometry, inertial properties (`<mass>`, `<inertia>`), collision shapes, and visual meshes directly in XML-based SDF format — without using helper tools like `xacro`.
- **Four-Wheel-Steering (FWS) Architecture:** Modeled a non-trivial kinematic configuration where all four wheels can be independently steered and driven.
- **Joint & Link Hierarchy:** Defined parent-child relationships between chassis, wheel links, and steering joints to reflect real mechanical constraints.
- **Physics Tuning:** Configured friction coefficients and contact parameters to reduce unrealistic simulation artifacts.

## 🚀 Usage
cd GAZEBO/gazebo_ws

# Source ROS 2 environment
source /opt/ros/jazzy/setup.bash

# Launch the simulation (package-specific launch file required)
gz sim src/gazebo_tutorial/buidling_robot.sdf
