N = int(input("Введите размер массива N: "))

A = []
for i in range(N):
    element = int(input(f"Введите элемент массива A[{i}]: "))
    A.append(element)

sum = 0
counter = 0
i = 0

while i < N:
    if i % 2 == 0:

        sum = sum + A[i]
        counter = counter + 1

    i = i + 1

if counter > 0:
    avg = sum / counter
else:
    avg = 0

print("Сумма элементов с чётными индексами:", sum)
print("Количество элементов с чётными индексами:", counter)
print("Среднее значение элементов с чётными индексами:", avg)