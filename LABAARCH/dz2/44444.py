def priority_encoder(X1, X2, X3, X4):
    if X1:
        a1, a2, EO = 0, 0, 0
    elif X2:
        a1, a2, EO = 0, 1, 0
    elif X3:
        a1, a2, EO = 1, 0, 0
    elif X4:
        a1, a2, EO = 1, 1, 0
    else:
        a1, a2, EO = 0, 0, 1
    return a1, a2, EO

# Пример использования
inputs = [
    (1, 0, 0, 0),
    (0, 1, 0, 0),
    (0, 0, 1, 0),
    (0, 0, 0, 1),
    (0, 0, 0, 0)
]

for X1, X2, X3, X4 in inputs:
    a1, a2, EO = priority_encoder(X1, X2, X3, X4)
    print(f"Вход: X1={X1}, X2={X2}, X3={X3}, X4={X4} -> Выход: a1={a1}, a2={a2}, EO={EO}")