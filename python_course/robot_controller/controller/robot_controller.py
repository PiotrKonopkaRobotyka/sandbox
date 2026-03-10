from hardware.hal import DCMotor
from monitor.robot_monitor import RobotMonitor

class RobotController:
    """Główny kontroler robota - łączy HAL i Monitor."""
    
    def __init__(self, config):
        # Diagnostyka
        self.monitor = RobotMonitor(config)
        
        # Silniki (Hardware)
        self.motor_left = DCMotor("LeftWheel", max_rpm=100)
        self.motor_right = DCMotor("RightWheel", max_rpm=100)
        
        # Inicjalizacja
        self.motor_left.enable()
        self.motor_right.enable()
    
    def process_command(self, command):
        """Wykonuje komendę na silnikach."""
        match command:
            case "CMD_STOP":
                print("[ACTION] Stopping motors")
                self.motor_left.control(0)
                self.motor_right.control(0)
            case "CMD_START":
                print("[ACTION] Moving forward")
                self.motor_left.control(70)
                self.motor_right.control(70)
            case "CMD_PAUSE":
                print("[ACTION] Slow mode")
                self.motor_left.control(30)
                self.motor_right.control(30)
            case _:
                print(f"[WARNING] Unknown: {command}")
    
    def check_system(self):
        """Sprawdza stan sensorów i zwraca alerty."""
        return self.monitor.check_sensors()