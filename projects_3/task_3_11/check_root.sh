#!/bin/bash
check_root() {
local current_uid="$EUID"
if [ "$current_uid" -ne 0 ]; then
    echo "Предупреждение: скрипт должен быть запущен с правами суперпользователя (root)."
    echo "Текущий UID: $current_uid. Работа скрипта прервана."
    exit 1  # Завершаем скрипт с кодом ошибки
  fi
echo "Проверка прав доступа пройдена: скрипт запущен от имени root (UID = $current_uid)."
}
check_root
echo "Выполнение основного кода скрипта..."

