MOV C, 2       ; m = 2 (пример)
MOV D, 1       ; n = 1

; Перемещение D в B через A
MOV A, D
MOV B, A       ; B = n

; Найти максимум из C (m) и B (n)
MOV A, C
CMP A, B
JNC C_GE_B     ; Если m >= n
MOV A, B       ; Максимум = n
JMP NEXT
C_GE_B:
MOV A, C       ; Максимум = m
NEXT:
MOV [0x00], A  ; Сохранить максимум в памяти

MOV A, 1       ; X = 1

LOOP:
; Проверка X <= максимума
CMP A, [0x00]
JC COMPUTE     ; Если X < максимума
JZ COMPUTE     ; Если X == максимума
JMP END_LOOP   ; Иначе завершить

COMPUTE:
; Вычисление (C-1)*X
MOV B, C       ; B = m
DEC B          ; B = m-1
MOV [0x01], 0  ; Обнулить результат
CMP B, 0
JZ SKIP_MULT   ; Если m-1 = 0, пропустить умножение

MULT_LOOP:
MOV C, [0x01]  ; Загрузить текущий результат
ADD C, A       ; C += X
MOV [0x01], C  ; Сохранить обратно
DEC B
JNZ MULT_LOOP  ; Если B ≠ 0, повторить цикл

SKIP_MULT:
; Проверка уравнения: n - (m-1)*X == 0
MOV B, [0x01]  ; B = (m-1)*X
MOV [0x02], D  ; [0x02] = n
MOV C, [0x02]
SUB C, B       ; C = n - B
CMP C, 0
JNZ NOT_ZERO   ; Если не ноль, продолжить
JMP END_LOOP   ; Выход при нахождении корня

NOT_ZERO:
INC A          ; X += 1
JMP LOOP

END_LOOP:
HLT