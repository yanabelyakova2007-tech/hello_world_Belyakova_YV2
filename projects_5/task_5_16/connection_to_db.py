import psycopg2
try:
    # Устанавливаем соединение
    connection = psycopg2.connect(
        host="localhost",          # База в контейнере, но доступна через localhost

        port="5433",               # Порт из секции ports

        user="postgres",           # POSTGRES_USER

        password="example",        # POSTGRES_PASSWORD

        database="testdb"          # POSTGRES_DB
    )
    print("Подключение к базе данных прошло успешно!")
except Exception as error:
    print(f"Ошибка при подключении: {error}")

