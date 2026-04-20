array = [7, 3, 8, 1, 4, 6, 2, 5]
print("Исходный массив:", array)

n = len(array)
for i in range(n):
    swapped = False
    for j in range(0, n - i - 1):
        if array[j] > array[j + 1]:
            array[j], array[j + 1] = array[j + 1], array[j]
            swapped = True
    if not swapped:
        break

print("Отсортированный массив:", array)