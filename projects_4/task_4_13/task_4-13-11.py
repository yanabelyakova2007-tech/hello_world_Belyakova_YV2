N = int(input("Введите размер массива N: "))
A = []
print("Введите элементы массива:")
for i in range(N):
    element = int(input(f"A[{i}] = "))
    A.append(element)

sum = 0
i = 0
count = 0  

while i < N:
   
    if i % 2 == 0: 
        sum = sum + A[i]  
        count += 1  

    i = i + 1

if count > 0:
    average = sum / count
else:
    average = 0 
    
print("Сумма элементов с чётными индексами:", sum)
print("Количество элементов с чётными индексами:", count)
print("Среднее арифметическое элементов с чётными индексами:", average)