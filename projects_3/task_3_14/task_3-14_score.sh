#!/bin/bash
echo "Студенты с оценкой выше 80:"
awk '$2 > 80 {print $0}' students.txt
echo "Студенты с оценкой ниже 70:"
awk '$2 < 70 {print $0}' students.txt
echo "Первая строка файла:"
awk 'NR == 1 {print $0}' students.txt

