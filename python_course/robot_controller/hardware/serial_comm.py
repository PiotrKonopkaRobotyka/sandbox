import time
import random

class SerialSimulator():
    def __init__(self):
        self.is_connected = False

    def connect(self):
        print ("Connecting to serial device...")
        time.sleep(2)
        self.is_connected = True
        print ("Connected")

    def read_line(self):
        if not self.is_connected:
            print(f"ERROR: Connection [{self.is_connected}]")
            return None

        toss = random.uniform(0.5, 2.0)
        time.sleep (toss)

        command = random.choice (["CMD_STOP", "CMD_START", "CMD_PAUSE"])

        return command


