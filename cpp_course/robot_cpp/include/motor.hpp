#pragma once
#include <string>
#include <string_view>  //Tylko odczyt bez alokacji
#include <cstdint> //Typu o konkretnum rozmiarze (int16_t)

class DCMotor {
public:
    //Konstruktor: nazwa, prędkość
    DCMotor(std::string_view name, int16_t max_rpm);

    //Metoda do ustawiania prędkości
    void setSpeed(int16_t speed);

    //Gettery (const = nie zmieniają stanu obiektu)
    //[[nodiscard]] - kompilator krzyczy jak zignorujesz wynik
    [[nodiscard]] std::string_view getName() const;
    [[nodiscard]] std::int16_t getSpeed() const;

private:
    std::string name_;
    int16_t max_rpm_;
    int16_t current_speed_ {0}; // Inicjalizacja zerem (Musi być!)
};
