a = float(input("Введите число a: "))
b = float(input("Введите число b: "))
c = float(input("Введите число c: "))
d = float(input("Введите число d: "))

min = a

if b < min:
    min = b

if c < min:
    min = c

if d < min:
    min = d

print("Минимальное число:", min)