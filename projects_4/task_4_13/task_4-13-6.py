N = int(input("Введите число N: "))  

sum = 0  
i = 1    

while i <= N:
    sum = sum + i * i  
    i = i + 1         

print("Сумма квадратов первых", N, "чисел равна:", sum)
