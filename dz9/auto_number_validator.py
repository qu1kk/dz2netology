import re

def validate_car_number(car_id):
    # Определяем регулярное выражение для валидного номера
    pattern = r'^[АВЕКМНОРСТУХЯ]\d{3}[АВЕКМНОРСТУХЯ]{2}\d{2,3}$'
    
    # Проверяем, соответствует ли строка шаблону
    match = re.match(pattern, car_id)
    
    if match:
        # Если номер валиден, выделяем сам номер и регион
        car_number = car_id[:6]  # Первые 6 символов: буква, 3 цифры, 2 буквы
        region = car_id[6:]  # Оставшиеся 2-3 цифры: регион
        return f"Номер {car_number} валиден. Регион: {region}."
    else:
        return "Номер не валиден."

# Пример использования:
car_id1 = 'А222BС96'
car_id2 = 'АБ22ВВ193'

print(validate_car_number(car_id1))  # Номер А222BС валиден. Регион: 96.
print(validate_car_number(car_id2))  # Номер не валиден.
