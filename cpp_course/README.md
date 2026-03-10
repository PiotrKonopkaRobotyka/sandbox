# 🖥️ C++ for Robotics — `robot_cpp`

![C++](https://img.shields.io/badge/C++-17/20-blue?logo=c%2B%2B)
![CMake](https://img.shields.io/badge/Build-CMake-green)

A standalone C++ application simulating a low-level robot controller. The project focuses on applying modern C++ idioms in the context of embedded robotics software — motor control, sensor abstraction, and hardware safety logic.

## 🏗️ Project Structure

# 🖥️ C++ for Robotics — `robot_cpp`

![C++](https://img.shields.io/badge/C++-17/20-blue?logo=c%2B%2B)
![CMake](https://img.shields.io/badge/Build-CMake-green)

A standalone C++ application simulating a low-level robot controller. The project focuses on applying modern C++ idioms in the context of embedded robotics software — motor control, sensor abstraction, and hardware safety logic.

## 🏗️ Project Structure

robot_cpp/
├── CMakeLists.txt
├── include/
│ ├── motor.hpp # DCMotor class definition
│ └── sensor.hpp # Sensor abstraction with SensorConfig & SensorType
└── src/
├── main.cpp # Robot Controller entry point
└── motor.cpp # DCMotor implementation

text

## 🎯 Key Implementations

- **Smart Pointers:** `std::unique_ptr<DCMotor>` for safe, non-owning motor management without raw `new`/`delete`.
- **Hardware Abstraction Layer (HAL):** `DCMotor` class encapsulates speed control with hard limit clamping (`setSpeed()` rejects values outside defined RPM range).
- **Sensor Abstraction:** `Sensor` class uses `SensorConfig` struct and `SensorType` enum for strongly-typed, configurable sensor initialization (LIDAR, IMU).
- **Emergency Stop Logic:** The main control loop evaluates `sensor.checkAlert()` on every reading. A threshold breach triggers an immediate `setSpeed(0)` — mimicking a real safety interrupt.
- **STL Containers:** `std::vector<Sensor>` with `emplace_back` for in-place sensor construction and range-based `for` loops for efficient iteration.

## ⚙️ Build & Run

```bash
cd cpp_course/robot_cpp
mkdir build && cd build
cmake ..
make
./robot_cpp
