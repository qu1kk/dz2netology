year = int(input('Введите год: '))
if year % 4 != 0:
    print('Обычный год.')
elif year % 100 == 0:
    if year % 400 == 0:
        print('Год високосный.')
    else:
        print('Обычный год.')
else:
    print('Год високосный.')