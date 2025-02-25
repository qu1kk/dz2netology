import numpy as np
import matplotlib.pyplot as plt

# Параметры сигнала
frequencies = [10000, 5000, 2000]  # Частоты в Гц
amplitude = 5  # Амплитуда
duration = 0.001  # Длительность визуализации в секундах (1 мс)
time_step = 0.000001  # Шаг моделирования в секундах (1 мкс)

# Запрещённая зона
lower_bound = 2
upper_bound = 4

# Время
t = np.arange(0, duration, time_step)

# Создание и визуализация сигналов
for freq in frequencies:
    # Треугольный сигнал
    triangle_signal = amplitude * np.abs(2 * (t * freq - np.floor(t * freq + 0.5)))
    
    # Цифровой сигнал
    digital_signal = np.where(triangle_signal > upper_bound, 5, np.where(triangle_signal < lower_bound, 0, np.nan))
    
    # Визуализация
    plt.figure(figsize=(10, 6))
    plt.plot(t, triangle_signal, label='Треугольный сигнал')
    plt.axhline(y=upper_bound, color='r', linestyle='--', label='Верхняя граница запрещённой зоны')
    plt.axhline(y=lower_bound, color='g', linestyle='--', label='Нижняя граница запрещённой зоны')
    plt.plot(t, digital_signal, 'k-', label='Цифровой сигнал', drawstyle='steps-post')
    plt.title(f'Треугольный сигнал {freq/1000} кГц')
    plt.xlabel('Время (с)')
    plt.ylabel('Амплитуда')
    plt.legend()
    plt.grid(True)
    plt.show()