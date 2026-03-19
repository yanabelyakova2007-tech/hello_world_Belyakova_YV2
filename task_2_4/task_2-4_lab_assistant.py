volume_input = input("Введите необходимый объем раствора (в мл): ")
volume = float(volume_input)

# 2. Рассчитываем необходимую массу соли (NaCl)
# Формула: масса = объем * 0.009
salt_mass = volume * 0.009

# 3. Рассчитываем объем воды (по условию, он равен общему объему)
water_volume = volume

# 4. Выводим результаты на экран
print("\n--- Результаты расчета ---")
print(f"Общий объем: {volume:.2f} мл")
print(f"Масса соли:  {salt_mass:.3f} г")
print(f"Объем воды:  {water_volume:.2f} мл")
print("-" * 26)

# 5. Сохраняем отчет в файл recipe.txt
file = open('recipe.txt', 'w', encoding='utf-8')
file.write("ОТЧЕТ ПО ПРИГОТОВЛЕНИЮ:\n")
file.write("-" * 23 + "\n")
file.write(f"Общий объем: {volume:.2f} мл\n")
file.write(f"Масса соли:  {salt_mass:.3f} г\n")
file.write(f"Объем воды:  {water_volume:.2f} мл\n")
file.close()
