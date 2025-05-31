import mmap
import multiprocessing

def producer(shmem, sem_empty, sem_full, message):
    # Ожидание освобождения буфера
    sem_empty.acquire()
    
    # Преобразование сообщения в байты
    data = message.encode('utf-8')
    length = len(data)
    
    # Запись длины сообщения и данных в буфер
    shmem.seek(0)
    shmem.write(length.to_bytes(4, byteorder='big'))
    shmem.write(data)
    
    # Сигнал о заполнении буфера
    sem_full.release()

def consumer(shmem, sem_empty, sem_full):
    # Ожидание заполнения буфера
    sem_full.acquire()
    
    # Чтение длины сообщения и данных
    shmem.seek(0)
    length_bytes = shmem.read(4)
    length = int.from_bytes(length_bytes, byteorder='big')
    data = shmem.read(length).decode('utf-8')
    
    # Вывод полученного сообщения
    print(f"Получено: {data}")
    
    # Сигнал об освобождении буфера
    sem_empty.release()

if __name__ == '__main__':
    # Размер буфера памяти (1024 байта)
    size = 1024
    
    # Создание буфера общей памяти
    shmem = mmap.mmap(-1, size)
    
    # Создание семафоров для синхронизации
    sem_empty = multiprocessing.Semaphore(1)  # Изначально буфер свободен
    sem_full = multiprocessing.Semaphore(0)   # Изначально буфер пуст
    
    # Создание процессов производителя и потребителя
    message = "Привет из производителя!"
    p_prod = multiprocessing.Process(
        target=producer, 
        args=(shmem, sem_empty, sem_full, message)
    )
    p_cons = multiprocessing.Process(
        target=consumer, 
        args=(shmem, sem_empty, sem_full)
    )
    
    # Запуск процессов
    p_prod.start()
    p_cons.start()
    
    # Ожидание завершения процессов
    p_prod.join()
    p_cons.join()
    
    # Закрытие буфера
    shmem.close()