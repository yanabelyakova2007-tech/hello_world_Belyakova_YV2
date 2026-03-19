print("=== Проверка совместимости групп крови ===\n")

# .strip() - удаляет пробелы в начале и конце
# .upper() - приводит к верхнему регистру для единообразия
donor = input("Введите группу крови донора (I, II, III, IV): ").strip().upper()
recipient = input("Введите группу крови пациента (I, II, III, IV): ").strip().upper()

if donor == recipient:
    print("✅ Переливание возможно: группы крови совпадают")
elif donor == "I":
    print("✅ Переливание возможно: донор с I (0) группой - универсальный донор")
elif donor == "II" and (recipient == "II" or recipient == "IV"):
    print("✅ Переливание возможно: кровь II группы совместима с II и IV")
elif donor == "III" and (recipient == "III" or recipient == "IV"):
    print("✅ Переливание возможно: кровь III группы совместима с III и IV")
elif donor == "IV" and recipient == "IV":
    print("✅ Переливание возможно: кровь IV группы совместима только с IV")
else:
    print("❌ Переливание НЕВОЗМОЖНО: группы крови несовместимы")