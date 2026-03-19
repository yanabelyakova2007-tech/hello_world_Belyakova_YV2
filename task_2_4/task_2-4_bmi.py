print("=== Анализ последовательности ДНК ===")
print()

sequence = input("Введите последовательность ДНК: ")

sequence_upper = sequence.upper()

print()
print("Последовательность в верхнем регистре:", sequence_upper)
print()

count_A = sequence_upper.count("A")
count_T = sequence_upper.count("T")
count_G = sequence_upper.count("G")
count_C = sequence_upper.count("C")

print("Подсчёт нуклеотидов:")
print("A:", count_A)
print("T:", count_T)
print("G:", count_G)
print("C:", count_C)
print()

total_length = len(sequence_upper)
print("Общая длина:", total_length, "нуклеотидов")
print()

percent_A = (count_A / total_length) * 100
percent_T = (count_T / total_length) * 100
percent_G = (count_G / total_length) * 100
percent_C = (count_C / total_length) * 100

print("Процентное содержание:")
print(f"A: {percent_A:.1f}%")
print(f"T: {percent_T:.1f}%")
print(f"G: {percent_G:.1f}%")
print(f"C: {percent_C:.1f}%")