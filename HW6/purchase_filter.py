import os
import platform
import json
import csv

# Функция для получения пути к рабочему столу на разных ОС
def get_desktop_path():
    system_name = platform.system()
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    if not os.path.exists(desktop_path):
        print(f"Рабочий стол не найден для ОС {system_name}, используется домашняя директория.")
        return os.path.expanduser("~")
    else:
        return desktop_path

# Функция для обработки JSON-файла visit_log.txt и создания funnel.csv
def process_visits(visit_log_path, funnel_path):
    saved_rows = 0  # Счётчик для записанных строк

    with open(visit_log_path, 'r', encoding='utf-8-sig') as f, open(funnel_path, 'w', encoding='utf-8-sig', newline='') as funnel_file:
        csv_writer = csv.writer(funnel_file, delimiter=',')
        csv_writer.writerow(["user_id", "category"])  # Записываем заголовок в CSV

        # Чтение первой строки для проверки на наличие заголовка
        first_line = f.readline().strip()
        
        # Проверяем, является ли первая строка заголовком
        try:
            first_record = json.loads(first_line)
            if "user_id" in first_record and "category" in first_record:
                print("Заголовок обнаружен в исходном файле, он будет пропущен.")
            else:
                # Если первая строка не заголовок, обрабатываем её как данные
                user_id = first_record.get("user_id")
                category = first_record.get("category")
                if user_id and category:
                    csv_writer.writerow([user_id, category])
                    saved_rows += 1  # Увеличиваем счётчик
        except json.JSONDecodeError:
            print("Ошибка чтения строки JSON:", first_line)

        # Обработка оставшихся строк
        for line in f:
            try:
                record = json.loads(line.strip())
                user_id = record.get("user_id")
                category = record.get("category")
                
                # Проверяем, что присутствуют и user_id, и category
                if user_id and category:
                    csv_writer.writerow([user_id, category])  # Записываем как отдельные столбцы
                    saved_rows += 1  # Увеличиваем счётчик
            except json.JSONDecodeError:
                print("Ошибка чтения строки JSON:", line.strip())

    print(f"Файл funnel.csv успешно создан на рабочем столе: {funnel_path}")
    print(f"Количество сохранённых строк: {saved_rows}")

# Основная функция для выполнения программы
def main():
    desktop_path = get_desktop_path()
    visit_log_path = os.path.join(desktop_path, 'visit_log.txt')
    funnel_path = os.path.join(desktop_path, 'funnel.csv')

    # Проверка наличия файла visit_log.txt
    if not os.path.exists(visit_log_path):
        print(f"Файл {visit_log_path} не найден. Поместите файл visit_log.txt на рабочий стол и запустите программу снова.")
        return
    
    # Проверка наличия файла funnel.csv
    if os.path.exists(funnel_path):
        print("Файл funnel.csv уже существует и будет перезаписан.")
    
    # Обработка визитов и создание funnel.csv
    process_visits(visit_log_path, funnel_path)

if __name__ == "__main__":
    main()