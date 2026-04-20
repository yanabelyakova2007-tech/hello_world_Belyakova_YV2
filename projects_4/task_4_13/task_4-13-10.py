N = int(input("Введите размер массива N: "))
A = []
print("Введите элементы массива:")
for i in range(N):
    element = int(input(f"A[{i}] = "))
    A.append(element)

sum = 0
i = 0

while i < N:
    if i % 2 == 1: 
        sum = sum + A[i]  
    
    i = i + 1

print("Сумма элементов с нечётными индексами:", sum)