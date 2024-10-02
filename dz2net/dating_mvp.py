# Все с парой
boys = ['Peter', 'Alex', 'John', 'Arthur', 'Richard']; boys = sorted(boys)
girls = ['Kate', 'Liza', 'Kira', 'Emma', 'Trisha']; girls = sorted(girls)

# Кто-то без пары
"""
boys = ['Peter', 'Alex', 'John', 'Arthur', 'Richard', 'Michael']; boys = sorted(boys)
girls = ['Kate', 'Liza', 'Kira', 'Emma', 'Trisha']; girls = sorted(girls)
"""
while len(boys) == len(girls):
    print('Результат\nИдеальные пары: ')
    for j in range(0, len(boys)):
        print(f'{boys[j]} и {girls[j]}')
    break
else:
    print('Кто-то останется без пары') 
