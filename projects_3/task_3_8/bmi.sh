#!/bin/bash
echo -n "Введите массу тела (кг): "
read mass
echo -n "Введите рост (м): "
read height
bmi=$(echo "scale=2; $mass / ($height * $height)" | bc)
bmi_int=$(printf "%.0f" $bmi)
echo "Ваша масса: $mass кг"
echo "Ваш рост: $height м"
echo "Индекс массы тела (ИМТ): $bmi"
echo "Целое значение ИМТ: $bmi_int"
