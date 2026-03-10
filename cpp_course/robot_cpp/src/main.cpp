#include <iostream>
#include <memory>  // Wymagane dla std::unique_ptr
#include <algorithm> // Do std::ranges
#include "motor.hpp"
#include "sensor.hpp"

int main() {
    std::cout << "--- Robot Controller ---\n";

    //Tworzenie silnika za pomocą inteligentnego wskaźnika
    //make_unique<Type>(args...) - bezpieczniejszy sposób tworzenia unikalnych wskaźników
    //'auto' domyśla się do właściwego typu std::unique_ptr<DCMotor>
    auto left_motor = std::make_unique<DCMotor>("Left Motor", 100);
    auto right_motor = std::make_unique<DCMotor>("Right Motor", 100);

    // 2. Testowanie logiki (Sterowanie)
    std::cout << "\n--- Testing Motor Control ---\n";
    //Używamy strzałki (->) do dostępu do metod przez wskaźnik inteligentny

    left_motor->setSpeed(50);
    right_motor->setSpeed(50);

    std::cout << "\n--- Increasing Speed Beyond Limits ---\n";
    left_motor->setSpeed(150);   // Przekroczenie maksymalnej prędkości
    right_motor->setSpeed(-120); // Przekroczenie minimalnej

    // 3.Odczyt (Getter)
    std::cout << "\n--- Current Motor States ---\n";
    std::cout << left_motor->getName() << " Speed: " << left_motor->getSpeed() << " RPM\n";
    std::cout << right_motor->getName() << " Speed: " << right_motor->getSpeed() << " RPM\n";

    // --- CZĘŚĆ 2: SENSORY (Nowość) ---
    std::cout << "\n--- Initializing Sensors ---\n";

    // Wektor przechowujący obiekty Sensor
    std::vector<Sensor> sensors;

    // Dodajemy sensory (emplace_back tworzy obiekt w miejscu)
    // Zauważ składnię: SensorConfig{...}
    sensors.emplace_back(SensorConfig{"FrontLidar", SensorType::Lidar, 0.0, 10.0});
    sensors.emplace_back(SensorConfig{"RearLidar",  SensorType::Lidar, 0.0, 5.0});
    sensors.emplace_back(SensorConfig{"MainIMU",    SensorType::Imu,   -2.0, 2.0});

    // Pętla odczytu (Monitor Loop)
    std::cout << "--- Reading Data ---\n";
    
    for (auto& sensor : sensors) {
        // 1. Odczyt
        double val = sensor.readValue();
        
        // 2. Logika
        std::cout << "Sensor: " << sensor.getName() << " | Value: " << val << "\n";
        
        // 3. Sprawdzenie bezpieczeństwa
        if (sensor.checkAlert(val)) {
            // Reakcja na awarię: ZATRZYMAJ SILNIKI!
            std::cout << "!!! EMERGENCY STOP TRIGGERED !!!\n";
            left_motor->setSpeed(0);
        }
    }

    // FILTROWANIE (Python: [s for s in sensors if type == LIDAR])
    std::cout << "\n--- Lidar Diagnostics ---\n";
    for (const auto& sensor : sensors) {
        if (sensor.getType() == SensorType::Lidar) {
            std::cout << " >> Diagnostics for LIDAR: " << sensor.getName() << "\n";
        }
    }

    return 0;

};
