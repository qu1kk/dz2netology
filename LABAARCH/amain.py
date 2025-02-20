import matplotlib.pyplot as plt
import numpy as np

# Параметры
t_end = 0.001  # Время моделирования (1 мс)
h = 1e-6       # Шаг по времени (1 мкс)
t = np.arange(0, t_end, h)  # Ось времени

# Логические уровни
logic_0 = 0.5
logic_1 = 4.5

# Запрещённые зоны
Umin1, Umax1 = 1.5, 3.5
Umin2, Umax2 = 2.0, 4.0

# Частоты сигналов
frequencies = [5000, 10000]  # 5 кГц и 10 кГц

# Постоянные времени
T1 = 0.00001
T2 = 0.00002

# Амплитуды помех
A1 = 0.1
A2 = 0.3

# Генерация входного сигнала (меандр)
def generate_signal(t, frequency):
    return 0.5 + 4.0 * (np.sin(2 * np.pi * frequency * t) > 0)

# Моделирование логического каскада
def logic_cascade(U_in, Umin, Umax):
    U_out = np.zeros_like(U_in)
    U_out[0] = logic_0  # Начальное состояние

    for i in range(1, len(U_in)):
        if U_out[i - 1] == logic_0:
            if U_in[i] > Umax:
                U_out[i] = logic_1
            else:
                U_out[i] = logic_0
        elif U_out[i - 1] == logic_1:
            if U_in[i] < Umin:
                U_out[i] = logic_0
            else:
                U_out[i] = logic_1
    return U_out

# Метод Эйлера для моделирования ёмкостной составляющей
def euler_method(Y, T):
    U = np.zeros_like(Y)
    U[0] = Y[0]  # Начальное условие

    for i in range(1, len(Y)):
        U[i] = U[i - 1] + h * (Y[i] - U[i - 1]) / T
    return U

# Добавление помехи
def add_noise(U, A):
    return U + A * np.random.uniform(-1, 1, size=len(U))

# Визуализация
def plot_signals(t, Y, U_in, U_out, title):
    plt.figure(figsize=(10, 6))
    plt.plot(t, Y, label="Входной сигнал (меандр)")
    plt.plot(t, U_in, label="Вход с ёмкостной составляющей")
    plt.plot(t, U_out, label="Выход логического каскада")
    plt.title(title)
    plt.xlabel("Время (с)")
    plt.ylabel("Напряжение (В)")
    plt.legend()
    plt.grid()
    plt.savefig(f"{title}.png")  # Сохраняем график в файл
    plt.close()  # Закрываем график

# Основной код
for freq in frequencies:
    # Генерация входного сигнала
    Y = generate_signal(t, freq)

    # Моделирование ёмкостной составляющей
    U_in_T1 = euler_method(Y, T1)
    U_in_T2 = euler_method(Y, T2)

    # Добавление помехи
    U_in_T1_noise = add_noise(U_in_T1, A1)
    U_in_T2_noise = add_noise(U_in_T2, A2)

    # Моделирование логического каскада
    U_out_T1 = logic_cascade(U_in_T1_noise, Umin1, Umax1)
    U_out_T2 = logic_cascade(U_in_T2_noise, Umin2, Umax2)

    # Визуализация результатов
    plot_signals(t, Y, U_in_T1_noise, U_out_T1, f"Частота {freq} Гц, T1 = {T1}, A1 = {A1}")
    plot_signals(t, Y, U_in_T2_noise, U_out_T2, f"Частота {freq} Гц, T2 = {T2}, A2 = {A2}")