N = int(input("Введите количество чисел N: "))  

max = 0  
i = 1    

while i <= N:
    x = int(input(f"Введите число №{i}: "))  
    
    if i == 1:
        max = x
        
    elif x > max:
        max = x
    
    i = i + 1  

print("Максимальное число:", max)