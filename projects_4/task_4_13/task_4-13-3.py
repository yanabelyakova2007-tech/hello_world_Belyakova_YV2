N = int(input("Введите число N: "))  

factorial = 1  
i = 1          

while i <= N:
    factorial = factorial * i  
    i = i + 1                  

print("Факториал числа", N, "равен:", factorial)