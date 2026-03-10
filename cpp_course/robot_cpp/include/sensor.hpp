#pragma once
#include <string>
#include <iostream>
#include <random> // Do generowania losowych danych (symulacja)

// 1. ENUM CLASS: Typ wyliczeniowy. 
// Bezpieczniejszy niż stringi. Kompilator nie pozwoli zrobić literówki.
enum class SensorType {
    Lidar,
    Imu,
    Camera
};

// 2. STRUCT: Kontener na dane konfiguracyjne.
// W C++ 'struct' to to samo co 'class', ale domyślnie wszystko jest publiczne.
// Idealne do trzymania "ustawień".
struct SensorConfig {
    std::string name;
    SensorType type;
    double min_val;
    double max_val;
};

// 3. KLASA LOGICZNA
class Sensor {
public:
    // Konstruktor
    explicit Sensor(SensorConfig config) : config_(std::move(config)) {}

    // Metoda symulująca odczyt
    [[nodiscard]] double readValue() {
        // Symulacja szumu (zwykła losowa liczba w zakresie +/- 10% od środka)
        // To tylko hack na potrzeby kursu, w prawdziwym robocie tu czytasz USB.
        double mid = (config_.min_val + config_.max_val) / 2.0;
        return mid + ((rand() % 100) / 10.0) - 5.0; 
    }

    // Metoda sprawdzająca, czy sensor działa poprawnie
    bool checkAlert(double value) const {
        if (value < config_.min_val || value > config_.max_val) {
            std::cout << "[ALERT] Sensor " << config_.name 
                      << " value " << value << " OUT OF RANGE!\n";
            return true;
        }
        return false;
    }

    // Getter typu (potrzebny do filtrowania!)
    [[nodiscard]] SensorType getType() const { return config_.type; }
    [[nodiscard]] std::string getName() const { return config_.name; }

private:
    SensorConfig config_;
};
