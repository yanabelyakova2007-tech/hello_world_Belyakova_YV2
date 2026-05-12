import psycopg2
import pandas as pd

# 1. Подключение к PostgreSQL-контейнеру
conn = None
try:
    conn = psycopg2.connect(
        host="localhost",
        port=5435,
        database="student",
        user="postgres_task",
        password="student"
    )
    print("Соединение установлено успешно!")

    # 2. Выполнение JOIN и загрузка в DataFrame
    query = """
        SELECT 
            p.name,
            p.category,
            pr.price,
            pr.created_at
        FROM prices pr
        JOIN products p ON pr.product_id = p.id
    """

    df = pd.read_sql(query, conn)

    print("\n--- Данные загружены ---")
    print(f"Загружено записей: {len(df)}")
    print(df.head())

    # 3. Базовые статистики по колонке price
    price = df['price']
    mean_price = price.mean()
    median_price = price.median()
    std_price = price.std()
    min_price = price.min()
    max_price = price.max()

    print("\n--- Общая статистика цен ---")
    print(f"Среднее значение: {mean_price:.2f} руб.")
    print(f"Медиана: {median_price:.2f} руб.")
    print(f"Стандартное отклонение: {std_price:.2f} руб.")
    print(f"Минимальная цена: {min_price:.2f} руб.")
    print(f"Максимальная цена: {max_price:.2f} руб.")

    # 4. Квартили, IQR и товары с ценой выше Q3
    Q1 = price.quantile(0.25)
    Q2 = price.quantile(0.50)
    Q3 = price.quantile(0.75)
    IQR = Q3 - Q1

    print("\n--- Квартили и размах ---")
    print(f"Q1 (первый квартиль): {Q1:.2f} руб.")
    print(f"Q2 (второй квартиль, медиана): {Q2:.2f} руб.")
    print(f"Q3 (третий квартиль): {Q3:.2f} руб.")
    print(f"Межквартильный размах (IQR): {IQR:.2f} руб.")

    outliers = df[df['price'] > Q3]
    print("\n--- Товары с ценой выше Q3 ---")
    if len(outliers) > 0:
        for _, row in outliers.iterrows():
            print(f"Товар: {row['name']}, Категория: {row['category']}, Цена: {row['price']:.2f} руб.")
    else:
        print("Нет товаров с ценой выше Q3")

    # 5. Группировка по категориям
    grouped = df.groupby('category')['price'].agg(
        count='count',
        mean='mean',
        median='median',
        std='std'
    ).round(2).sort_values(by='mean', ascending=False)

    print("\n--- Статистика по категориям (отсортировано по убыванию средней цены) ---")
    print(grouped)

    # 6. Разброс цен по каждому товару
    price_range = df.groupby('name')['price'].agg(min_price='min', max_price='max')
    price_range['price_span'] = price_range['max_price'] - price_range['min_price']
    top_5_variance = price_range.sort_values(by='price_span', ascending=False).head(5)

    print("\n--- Топ-5 товаров с наибольшим разбросом цен ---")
    print(top_5_variance[['min_price', 'max_price', 'price_span']].round(2))

except psycopg2.Error as e:
    print(f"Ошибка подключения к базе данных: {e}")
except Exception as e:
    print(f"Произошла ошибка: {e}")
finally:
    if conn:
        conn.close()
        print("\nСоединение закрыто.")
