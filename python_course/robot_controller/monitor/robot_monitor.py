import random

class RobotMonitor:
    def __init__(self, config):
        """
        Inicjalizacja monitora robota.
        :param config: Słownik z konfiguracją (z json.load)
        """
        # Używamy .get(), żeby program działał nawet przy braku nazwy w pliku
        self.name = config.get("robot_name", "UnknownRobot")
        
        # Jeśli nie ma sensorów, wstawiamy pustą listę, żeby pętla for się nie wywaliła
        self.sensors = config.get("sensors", [])

        self.version = config.get("version", "1.0")
        
        self.update_rate = config.get("update_rate", 60)  # Domyślnie 60 Hz
        self.status = "Initializing"

    def __str__(self):
        """
        Reprezentacja tekstowa obiektu.
        Wywoływana, gdy zrobisz print(robot_instance).
        """
        sensor_count = len(self.sensors)
        return f"Robot: {self.name} | Status: {self.status} | Version: {self.version} | Sensors Active: {sensor_count}"

    def check_sensors(self):
        """
        Sprawdza status wszystkich sensorów i aktualizuje status robota.
        """
        alerts = [] # Lista na komunikaty błędów

        for sensor in self.sensors:
            # Iterujemy po liście słowników (każdy sensor to osobny słownik)
            name = sensor.get("name", "Unknown")
            safe_range= sensor.get("safe_range", [0.0, 10.0]) #Domyślny zakres jeśli brak w JSON
            safe_min, safe_max = safe_range[0], safe_range [1]
            
            # 1. SYmulacja odczytu liczby zmiennoprzecinkowej
            # Losowanie wartości od -5 do 15 aby zasymulować wyjście poza zakres 
            curren_value = random.uniform(safe_min-5.0, safe_max+5.0)

            print (f"Sensor: {name:<15} | Value: {curren_value:6.2f} | Range: {safe_range}")

            # 2. Sprawdzanie limitów
            if not (safe_min <= curren_value <= safe_max):
                alert_msg = f"ALERT: {name} value {curren_value:.2f} out of range [{safe_min}, {safe_max}]"
                alerts.append(alert_msg)

        return alerts
    
    def sensor_filter(self, sensor_type):
         return [s["name"] for s in self.sensors if s["type"] == sensor_type]