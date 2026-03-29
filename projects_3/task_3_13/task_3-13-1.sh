#!/bin/bash
sed -i 's|/var/lib/mysql/data|/mnt/ssd/mysql|g' settings.php

echo "Замена пути в settings.php завершена."
