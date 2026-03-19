total_capsules = int(input("Введите общее количество произведенных капсул: "))
capacity = int(input("Введите количество капсул в одной упаковке: "))

full_packages = total_capsules // capacity
remaining_capsules = total_capsules % capacity

print("\n--- Отчет фасовочного цеха ---")
print(f"Полных упаковок: {full_packages}")
print(f"Остаток капсул: {remaining_capsules}")