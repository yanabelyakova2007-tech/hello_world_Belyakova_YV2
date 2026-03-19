weight = float(input("Введите ваш вес (кг): "))
height_cm = float(input("Введите ваш рост (см): "))

height_m = height_cm / 100

bmi = weight / (height_m ** 2)


print("\n--- Отчет о состоянии здоровья ---")
print(f"Рост:\t{height_cm:.1f} cm")
print(f"Вес:\t{weight:.1f} кг")
print(f"Индекс массы тела:\t{bmi:.2f}")
