#!/bin/bash
echo -n "Введите год вашего рождения: "
read birth_year
echo -n "Введите текущий год: "
read current_year
age=$(( current_year - birth_year ))
echo "Год рождения: $birth_year"
echo "Текущий год: $current_year"
echo "Ваш возраст: $age лет"
