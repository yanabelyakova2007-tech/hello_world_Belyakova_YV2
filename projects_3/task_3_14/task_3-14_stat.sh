#!/bin/bash
sum=$(awk '{sum += $2} END {print sum}' students.txt)
average=$(awk '{sum += $2; count++} END {print sum/count}' students.txt)
max=$(awk 'NR==1{max=$2} $2>max{max=$2} END{print max}' students.txt)

echo "Сумма всех оценок: $sum"
echo "Средняя оценка: $average"
echo "Максимальная оценка: $max"
