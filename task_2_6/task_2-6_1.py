pH = float(input("Введите значение pH: "))

# Используем if/elif/else для определения среды
if pH < 7:
    print("Кислая среда")
elif pH == 7:
    print("Нейтральная среда")
else:  # pH > 7
    print("Щелочная среда")