reagent_name = input("Введите название нового реактива: ")
quantity = input("Введите количество реактива: ")

f = open("inventory.txt", "w", encoding="utf-8")
print(f"Реактив {reagent_name} поступил на склад в количестве {quantity} шт.", file=f)
f.close()