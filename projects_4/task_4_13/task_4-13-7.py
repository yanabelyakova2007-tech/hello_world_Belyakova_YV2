N = int(input("Введите размер массива N: "))  

A = []
for i in range(N):
    element = float(input(f"Введите элемент массива A[{i}]: "))
    A.append(element)

S = 0  

for i in range(N):
    S = S + A[i]  

average = S / N

print("Среднее арифметическое элементов массива:", average)