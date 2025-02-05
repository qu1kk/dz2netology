#include <iostream>
#include <cmath> // для использования функции sqrt

int main() {
    // Объявление переменных для координат точек
    float xa, ya;
    float xb, yb;
    float xc, yc;

    // Приглашение на ввод данных
    std::cout << "Введите координаты точки A (xa ya): ";
    std::cin >> xa >> ya;

    std::cout << "Введите координаты точки B (xb yb): ";
    std::cin >> xb >> yb;

    std::cout << "Введите координаты точки C (xc yc): ";
    std::cin >> xc >> yc;

    // Вычисление длин сторон треугольника
    float ab = sqrt(pow(xb - xa, 2) + pow(yb - ya, 2)); // Длина стороны AB
    float bc = sqrt(pow(xc - xb, 2) + pow(yc - yb, 2)); // Длина стороны BC
    float ca = sqrt(pow(xa - xc, 2) + pow(ya - yc, 2)); // Длина стороны CA

    // Вычисление периметра треугольника
    float perimeter = ab + bc + ca;

    // Вычисление площади треугольника по формуле Герона
    float s = perimeter / 2; // Полупериметр
    float area = sqrt(s * (s - ab) * (s - bc) * (s - ca));

    // Вывод результатов
    std::cout << "Периметр треугольника: " << perimeter << std::endl;
    std::cout << "Площадь треугольника: " << area << std::endl;

    return 0;
}