#include <iostream>      // Do wypisywania na ekran
#include <algorithm>     // Do std::clamp (przycinanie wartości)
#include "motor.hpp"  

DCMotor::DCMotor(std::string_view name, int16_t max_rpm)
    : name_(name), max_rpm_(max_rpm) {
    std::cout << "[HAL] Motor initialized: " << name_ << "Max RPM: " << max_rpm_ << ")\n";
}

//Implementacja setSpeed
void DCMotor::setSpeed(int16_t speed) {
    // Logika limitowania prędkości (coś jak if w Pythonie)
    int16_t safe_speed = std::clamp(speed, (int16_t)-max_rpm_, max_rpm_);

    //Aktualizacja stanu
    current_speed_ = safe_speed;

    //Symulacja wysłania komendy do silnika
    if (safe_speed != speed) {
        std::cout << "[WARNING]" << name_ << " limited from " << speed << " to " << safe_speed << "\n";
    }
    std::cout << "[" << name_ << "] Speed set to " << current_speed_ << " RPM\n";
}

//Gettery
std::string_view DCMotor::getName() const {
    return name_;
}

int16_t DCMotor::getSpeed() const {
    return current_speed_;
}
