## 📄 `python_course/README.md`

```markdown
# 🐍 Python for Robotics — `robot_controller`

![Python](https://img.shields.io/badge/Python-3.12-green?logo=python)

A modular, multithreaded robot controller application implemented in Python. The project mirrors real robotics software architecture — Hardware Abstraction Layer, asynchronous serial communication, a live monitoring system, and JSON-based configuration management.

## 🏗️ Project Structure

    robot_controller/
    ├── main.py # Application entry point (CLI + main loop)
    ├── config.py # JSON config loader
    ├── config_example.json # Example robot configuration
    ├── hardware/
    │ ├── hal.py # DCMotor Hardware Abstraction Layer
    │ └── serial_comm.py # Serial communication simulator
    ├── controller/
    │ └── robot_controller.py # Command processor & safety checker
    └── monitor/
    └── robot_monitor.py # Robot state monitor & sensor filter


## 🎯 Key Implementations

- **Hardware Abstraction Layer (HAL):** `DCMotor` class enforces `enable()`/`disable()` state machine before accepting speed commands — prevents commanding a disabled actuator.
- **Multithreaded Architecture:** Serial communication runs in a dedicated `daemon` thread using `threading.Thread`. Data is passed to the main loop via `queue.Queue` (Producer-Consumer pattern), preventing I/O blocking.
- **Non-Blocking Main Loop:** Uses `cmd_queue.get_nowait()` inside a `try/except queue.Empty` block — the control loop never stalls waiting for serial input.
- **CLI with `argparse`:** Supports `--verbose` flag and `--config` parameter for runtime configuration injection without recompiling.
- **JSON Configuration:** Robot parameters (sensors, motors, thresholds) are externalized to `config_example.json` and loaded via `load_config()`, following the separation of data from logic.
- **Graceful Shutdown:** `KeyboardInterrupt` handler ensures a clean `sys.exit(0)` — critical in robotic systems to prevent hardware in undefined state.

## 🚀 Usage
    cd python_course/robot_controller

# Standard run
    python3 main.py

# With verbose diagnostics and custom config
    python3 main.py --verbose --config config_example.json