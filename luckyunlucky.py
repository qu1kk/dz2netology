number = [int(i) for i in input()]
if sum(number[:3]) == sum(number[3:]):
    print('Удачный билет ')
else:
    print('Неудачный билет')