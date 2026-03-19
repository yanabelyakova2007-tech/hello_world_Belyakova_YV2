files = ["seq1", "seq2", "seq3", "seq4"]

date = "2026-03-19"

print("Обработка файлов с образцами:")
print("-" * 30)

for name in files:
    new_name = name + "_" + date + ".fasta"
    print(f"Файл: {new_name}")

print("-" * 30)
print("Готово!")