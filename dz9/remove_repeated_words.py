import re

def remove_repeated_words(some_string):
    # Регулярное выражение для поиска повторяющихся слов
    pattern = r'\b(\w+)(?:\s+\1)+\b'
    # Замена повторяющихся слов на одно их появление
    result = re.sub(pattern, r'\1', some_string, flags=re.IGNORECASE)
    return result

# Пример использования
some_string = ('Напишите функцию функцию, которая будет будет будет будет '
               'удалять все все все все последовательные повторы слов из из из из '
               'заданной строки строки при помощи регулярных выражений')

result = remove_repeated_words(some_string)
print(result)