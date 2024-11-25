import time
from concurrent.futures import ThreadPoolExecutor

# Функция для формулы 1
def formula_1(x):
    return x**2 - x**2 + x**4 - x**5 + x + x

# Функция для формулы 2
def formula_2(x):
    return x + x

# Функция для формулы 3
def formula_3(result_1, result_2):
    return result_1 + result_2

# Функция для выполнения итераций и замера времени
def run_iterations(iterations):
    # Список значений для вычислений (например, от 0 до iterations-1)
    data = range(iterations)
    
    # Шаг 1: Параллельное выполнение формулы 1
    start_step1 = time.time()
    with ThreadPoolExecutor() as executor:
        results_1 = list(executor.map(formula_1, data))
    duration_step1 = time.time() - start_step1

    # Шаг 2: Параллельное выполнение формулы 2
    start_step2 = time.time()
    with ThreadPoolExecutor() as executor:
        results_2 = list(executor.map(formula_2, data))
    duration_step2 = time.time() - start_step2

    # Шаг 3: Последовательное выполнение формулы 3
    start_step3 = time.time()
    results_3 = [formula_3(r1, r2) for r1, r2 in zip(results_1, results_2)]
    duration_step3 = time.time() - start_step3

    return duration_step1, duration_step2, duration_step3

# Запуск вычислений для 10 000 и 100 000 итераций
iterations_list = [10_000, 100_000]
for iterations in iterations_list:
    print(f"\nВыполнение для {iterations} итераций:")
    step1_time, step2_time, step3_time = run_iterations(iterations)
    print(f"Шаг 1 (формула 1): {step1_time:.4f} секунд")
    print(f"Шаг 2 (формула 2): {step2_time:.4f} секунд")
    print(f"Шаг 3 (формула 3): {step3_time:.4f} секунд")
