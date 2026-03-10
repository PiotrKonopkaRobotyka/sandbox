import sys
import threading
import argparse
import queue
import time
from config import load_config
from monitor.robot_monitor import RobotMonitor
from hardware.hal import DCMotor
from hardware.serial_comm import SerialSimulator
from controller.robot_controller import RobotController

def serial_worker(serial_dev, data_queue):
    #Funkcja działa w osobnym wątku
    print("[THREAD] Worker started")
    while True:
        data = serial_dev.read_line()
        if data:
            # Wrzucamy do kolejki
            data_queue.put(data)

def main():

    #HAL test
    print ("\n--- Testing HAL ---")

    motor1 = DCMotor("LeftWheel", min_rpm = 10, max_rpm=100)
    
    #Próba sterowania wyłączonym silnikiem
    motor1.control(40)

    #Włączenie i sterowanie
    motor1.enable()
    motor1.control(50)

    #Przekroczenie limitu
    motor1.control(101)
    motor1.control(9)

    print ("\n--- Test Complete")

    #Async
    print("\n--- Testing Async Communication ---")
    
    #Deklaracja urządzenia i połączenia
    sim_serial = SerialSimulator()
    sim_serial.connect()

    cmd_queue = queue.Queue()     #Nowa kolejka

    #Deklaracja wątku; target-funkcja, args-argumenty.
    comm_thread = threading.Thread(target=serial_worker, args=(sim_serial, cmd_queue), daemon=True) 
    comm_thread.start()    #Uruchomienie 

    print("--- Continue Main Thread ---")

    # Konfiguracja parsera argumentów
    parser = argparse.ArgumentParser(description="Robot State Monitor CLI")

    # Dodajemy flagę
    parser.add_argument("--verbose", action="store_true", help="Print detailed debug info")
    parser.add_argument("--config", type=str, default="config_example.json", help="Path to JSON config file")
    
    args = parser.parse_args()# Parsowanie

    config = load_config(args.config)

    # Użycie argumentu (args.config zamiast sztywnej nazwy)
    if args.verbose:
        print("Verbose mode enabled")
        print(f"VERBOSE: {config}")

    else:
        print(f"Starting monitor using config: {args.config}")

    # Guard clause - jeśli config pusty, wychodzimy
    if not config:
        print("Error: Could not load configuration.")
        sys.exit(1)

    try:
        robot = RobotMonitor(config)
        print("\n--- Initialization Successful ---")
        print(robot)

        #Test filtrowania
        lidars  = robot.sensor_filter("LIDAR")
        print(f"\nFound {len(lidars)} LIDARs: {lidars}")

        robot_system = RobotController(config)

        #Główna pętla
        while True:
            #Obsługa komend z wątku (Consumer)
            try: 
                #Wyjmuje z kolejki i nie czeka (nie blokuje)
                command = cmd_queue.get_nowait()

                print(f"\n[MAIN] Received command: {command}")

                robot_system.process_command(command) 

            except queue.Empty:
                pass #Pusto w kolejce

            #Sprawdzanie sensorów
            alerts = robot_system.check_system()
            if alerts:
                print(f"\n!!! SYSTEM WARNINGS !!!")
                for a in alerts:
                    print(a)

            time.sleep(3) #1HZ

    except KeyboardInterrupt:
        print("\n[MAIN] Stopping robot...")
        sys.exit(0)
    except Exception as e:
        print(f"Error initializing robot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
