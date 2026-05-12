import psycopg2



connection = None

cursor = None



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

    # Выполняем обновление

    cursor.execute("UPDATE courses SET credits = 5 WHERE course_id = 1;")



    # КРИТИЧЕСКИ ВАЖНО: фиксируем изменения в базе

    connection.commit()

    print("Данные успешно обновлены!")



except Exception as error:

    if connection:

        # Если что-то пошло не так, отменяем всё (откат)

        connection.rollback()

    print(f"Ошибка: {error}")



finally:

    if cursor is not None:

        cursor.close()

    if connection is not None:

        connection.close()

