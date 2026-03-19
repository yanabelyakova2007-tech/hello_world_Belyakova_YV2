sequences = ["ATATACGCGTA", "CTTCGGNGGA"]

print("=== Анализ последовательностей ===\n")

for seq in sequences:
    print(f"Последовательность: {seq}")
    print("Построчный вывод:")
    
    for letter in seq:
        print(letter)
    
    print("-" * 20) 

print("Цикл выполнен")