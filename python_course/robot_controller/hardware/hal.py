from abc import ABC, abstractmethod

class Actuator(ABC):

    """Abstrakcyjna klasa reprezentująca aktuator w systemie HAL.
    Wymusza, aby wszystkie silinki/siłowniki miały metodę control() i get_state().
    """

    def __init__(self, name):
        self.name = name
        self._is_active = False #Zmienna prywatna przechowująca stan aktuatora.

    def enable(self):
        #Włącza aktuator.
        self._is_active = True
        print(f"[{self.name}] ENABLED")

    def disabled(self):
        #Wyłącz aktuator.
        self._is_active = False
        print (f"[{self.name} DISABLED]")

    @abstractmethod
    def control(self, value):
        #Metoda abstrakcyjna. Każdy silnik musi zdefiniować, co robi z wartością sterującą.
        pass

class DCMotor(Actuator):
    def __init__(self, name, min_rpm = 30, max_rpm=100):
        super().__init__(name) #Wywołanie konstruktora rodzica
        self.min_rpm = min_rpm
        self.max_rpm = max_rpm

    def control(self, value):
        #Steruje prędkością silnika i uwzględnia limity
        if not self._is_active: #Sprawdzenie czy włączony
            print (f"ERROR: [{self.name}] is disabled.")
            return 
        
        #Limitowanie (Clamping)
        #Jeśli value > max_rpm, ustaw max_rpm. Jeśli < min_rpm, ustam min_rpm

        if value > self.max_rpm:
            print (f"WARNING: Limiting {value} to MAX {self.max_rpm} RPM")
            value = self.max_rpm
        elif value < self.min_rpm:
            print (f"WARNING: Limiting {value} to MIN {self.min_rpm} RPM")
            value = self.min_rpm

        #Symulacja działąnia
        print (f"[{self.name}] spinning at {value} RPM")
