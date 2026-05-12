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

    cursor = connection.cursor()
    # 1. Выполняем запрос
    cursor.execute("SELECT first_name, last_name FROM students;")
    # 2. Извлекаем все строки
    students = cursor.fetchall()
    for student in students:
        print(f"Студент: {student[0]} {student[1]}")
    # Не забываем закрыть курсор
    cursor.close()

except Exception as error:
    print(f"Ошибка при подключении: {error}")