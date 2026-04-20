N = int(input("Введите размер массива N: "))  

A = []
for i in range(N):
    element = float(input(f"Введите элемент массива A[{i}]: "))
    A.append(element)

K = 0  

for i in range(N):
    if A[i] > 0:  
        K = K + 1  

print("Количество положительных чисел в массиве:", K)