import os
import sys
import stat
import platform
from datetime import datetime

def print_filesystem_info(path='.'):
    """Выводит информацию о файловой системе"""
    system = platform.system()
    print(f"\nИнформация о файловой системе для: {os.path.abspath(path)}")
    print(f"Тип ОС: {system}")
    
    try:
        if system == 'Windows':
            # Для Windows: объемные характеристики
            total, used, free = (v // (1024*1024) for v in os.statvfs(path)[:3])
            print(f"Общий размер: {total} МБ")
            print(f"Использовано: {used} МБ")
            print(f"Свободно: {free} МБ")
        else:
            # Для Unix-систем: полная информация
            fs = os.statvfs(path)
            print(f"Тип ФС: {os.popen(f'df -T {path} | awk \'NR==2{{print $2}}\'').read().strip()}")
            print(f"Размер блока: {fs.f_bsize} байт")
            print(f"Количество блоков: {fs.f_blocks}")
            print(f"Свободных блоков: {fs.f_bfree}")
            print(f"Доступно блоков: {fs.f_bavail}")
            print(f"Inodes: {fs.f_files}")
            print(f"Свободные inodes: {fs.f_ffree}")
    except Exception as e:
        print(f"Ошибка при получении информации о ФС: {e}")

def print_file_info(filepath):
    """Выводит информацию о файле"""
    print(f"\nИнформация о файле: {filepath}")
    
    try:
        st = os.stat(filepath)
        file_stat = stat.filemode(st.st_mode)
        file_type = "Директория" if stat.S_ISDIR(st.st_mode) else \
                   "Файл" if stat.S_ISREG(st.st_mode) else \
                   "Символическая ссылка" if stat.S_ISLNK(st.st_mode) else \
                   "Блочное устройство" if stat.S_ISBLK(st.st_mode) else \
                   "Сокет" if stat.S_ISSOCK(st.st_mode) else "Другой тип"

        print(f"Inode: {st.st_ino}")
        print(f"Тип: {file_type}")
        print(f"Права доступа: {file_stat}")
        print(f"Размер: {st.st_size} байт")
        print(f"Время создания: {datetime.fromtimestamp(st.st_ctime)}")
        print(f"Последнее изменение: {datetime.fromtimestamp(st.st_mtime)}")
        print(f"Последний доступ: {datetime.fromtimestamp(st.st_atime)}")
    except Exception as e:
        print(f"Ошибка при получении информации о файле: {e}")

def compare_filesystems():
    """Сравнивает информацию для разных файловых систем"""
    print("\nСравнение файловых систем:")
    
    # Примеры путей для разных ОС
    paths = {
        'Linux': '/',
        'Darwin': '/',
        'Windows': 'C:\\'
    }
    
    current_system = platform.system()
    path = paths.get(current_system, '.')
    
    print_filesystem_info(path)
    
    # Выводим информацию о системном файле
    if current_system == 'Windows':
        example_file = os.path.join(os.environ['WINDIR'], 'explorer.exe')
    elif current_system == 'Linux':
        example_file = '/etc/passwd'
    elif current_system == 'Darwin':
        example_file = '/etc/hosts'
    else:
        example_file = __file__  # Текущий скрипт
    
    if os.path.exists(example_file):
        print_file_info(example_file)
    else:
        print(f"Файл {example_file} не найден")
        print_file_info(__file__)

if __name__ == "__main__":
    # Вывод основной информации
    print_filesystem_info()
    print_file_info(__file__)
    
    # Дополнительное сравнение для разных ФС
    compare_filesystems()