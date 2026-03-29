#!/bin/bash

echo "Анализ использования дискового пространства:"
echo "----------------------------------------"

df -h | awk '
NR > 1 {
    filesystem = $1
    usage_percent = $5
 gsub(/%/, "", usage_percent)
  print filesystem ": " usage_percent "%"
 if (usage_percent + 0 > 90) {
        print "  ПРЕДУПРЕЖДЕНИЕ: " filesystem " заполнена на " usage_percent "% — требуется внимание!"
    }
}
'
