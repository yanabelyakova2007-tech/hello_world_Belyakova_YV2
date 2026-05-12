import psycopg2

def main():
    connection = None
    cursor = None

    try:
        # 1. Устанавливаем соединение с базой данных
        connection = psycopg2.connect(
            host="localhost",          # Хост, где запущена БД (например, localhost или IP-адрес)
            port="5433",               # Порт PostgreSQL (по умолчанию 5432)
            user="postgres",           # Имя пользователя для подключения
            password="example",       # Пароль пользователя
            database="testdb"         # Название базы данных
        )
        print("Соединение с базой данных установлено успешно!")

        # 2. Создаём курсор для работы с БД
        cursor = connection.cursor()

        # 3. Выполняем SQL-запрос
        sql_query = "SELECT course_id, course_name, credits FROM courses;"
        cursor.execute(sql_query)

        # 4. Извлекаем и выводим результаты запроса
        rows = cursor.fetchall()
        print("\nСписок курсов:")
        for row in rows:
            print(f"ID курса: {row}, Название: {row}, Кредиты: {row}")

    except Exception as error:
        # 5. Обработка ошибок (если соединение или запрос не выполнились)
        print(f"Произошла ошибка: {error}")

    finally:
        # 6. Закрываем курсор и соединение с БД (даже если была ошибка)
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("Соединение с базой данных закрыто.")

if __name__ == "__main__":
    main()