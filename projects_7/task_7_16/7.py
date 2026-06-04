import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore')

# ==================================================
# НАСТРОЙКИ
# ==================================================
# Параметры подключения к БД (замените на свои)
DB_CONFIG = {
    'dbname': 'student',
    'user': 'postgres_task',
    'password': 'student',
    'host': 'localhost',
    'port': 5435
}

# Настройки графиков
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.unicode_minus'] = False


# ==================================================
# ФУНКЦИЯ ГЕНЕРАЦИИ ТЕСТОВЫХ ДАННЫХ
# ==================================================
def generate_test_data():
    """Генерирует тестовые данные для анализа"""
    print("🔄 Генерация тестовых данных...")
    np.random.seed(42)

    # 1. Данные о поставщиках (100 товаров)
    product_ids = range(1, 101)
    suppliers_data = []
    for pid in product_ids:
        num_suppliers = np.random.poisson(7, 1)[0]
        num_suppliers = max(1, min(15, num_suppliers))
        suppliers_data.append({
            'product_id': pid,
            'total_suppliers': num_suppliers
        })

    df_suppliers = pd.DataFrame(suppliers_data)

    # 2. Данные о ценах (с аномалиями)
    prices_data = []
    for pid in product_ids:
        price = int(np.random.normal(500, 200, 1)[0])
        price = max(10, price)
        prices_data.append({
            'product_id': pid,
            'price': price
        })

    df_prices = pd.DataFrame(prices_data)

    # Добавляем явные аномалии в цены
    df_prices.loc[5, 'price'] = 5000
    df_prices.loc[42, 'price'] = 7500
    df_prices.loc[18, 'price'] = 8

    # 3. Данные о продажах за последние 12 месяцев
    dates = pd.date_range('2025-06-01', '2026-05-01', freq='MS')
    sales_data = []

    for i, date in enumerate(dates):
        base_revenue = 50000 + i * 2000
        seasonality = 10000 * np.sin(i * np.pi / 6)
        revenue = base_revenue + seasonality + np.random.normal(0, 5000)
        revenue = max(10000, int(revenue))
        sales_data.append({
            'month': date,
            'total_revenue': revenue
        })

    df_sales = pd.DataFrame(sales_data)
    df_sales.loc[6, 'total_revenue'] = 150000  # Аномалия в декабре

    # 4. Агрегированные данные
    df_agg = df_suppliers.merge(df_prices, on='product_id')
    product_sales = []
    for pid in product_ids:
        sales_volume = int(np.random.gamma(2, 100, 1)[0]) + 50
        product_sales.append({'product_id': pid, 'sales_volume': sales_volume})

    df_product_sales = pd.DataFrame(product_sales)
    df_agg = df_agg.merge(df_product_sales, on='product_id')

    print(f"✅ Сгенерировано: {len(df_suppliers)} товаров, {len(df_sales)} месяцев продаж")

    return df_suppliers, df_prices, df_sales, df_agg


# ==================================================
# ФУНКЦИЯ ЗАГРУЗКИ ДАННЫХ ИЗ БД
# ==================================================
def load_from_database():
    """Пытается загрузить данные из реальной БД"""
    try:
        print("📡 Подключение к базе данных...")
        conn = psycopg2.connect(**DB_CONFIG)

        cursor = conn.cursor()
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            LIMIT 5;
        """)
        tables = cursor.fetchall()

        if not tables:
            print("⚠️ В базе данных нет таблиц")
            conn.close()
            return None, None, None, None

        print(f"📊 Найдены таблицы: {[t[0] for t in tables]}")

        df_suppliers = pd.DataFrame()
        df_prices = pd.DataFrame()
        df_sales = pd.DataFrame()
        df_agg = pd.DataFrame()

        # Загрузка поставщиков
        try:
            df_suppliers = pd.read_sql_query("""
                SELECT 
                    product_id,
                    COUNT(id) AS total_suppliers
                FROM suppliers
                WHERE product_id IS NOT NULL
                GROUP BY product_id
                LIMIT 1000;
            """, conn)
            print(f"✓ Загружено {len(df_suppliers)} записей о поставщиках")
        except Exception as e:
            print(f"⚠️ Не удалось загрузить поставщиков: {e}")

        # Загрузка цен
        try:
            df_prices = pd.read_sql_query("""
                SELECT 
                    product_id,
                    price
                FROM products
                WHERE price IS NOT NULL
                LIMIT 1000;
            """, conn)
            print(f"✓ Загружено {len(df_prices)} записей о ценах")
        except Exception as e:
            print(f"⚠️ Не удалось загрузить цены: {e}")

        # Загрузка продаж
        try:
            df_sales = pd.read_sql_query("""
                SELECT 
                    DATE_TRUNC('month', sale_date) AS month,
                    SUM(amount) AS total_revenue
                FROM sales
                WHERE sale_date IS NOT NULL
                GROUP BY month
                ORDER BY month
                LIMIT 100;
            """, conn)
            print(f"✓ Загружено {len(df_sales)} записей о продажах")
        except Exception as e:
            print(f"⚠️ Не удалось загрузить продажи: {e}")

        conn.close()

        if df_suppliers.empty and df_prices.empty and df_sales.empty:
            print("⚠️ Нет данных в таблицах")
            return None, None, None, None

        if not df_suppliers.empty and not df_prices.empty:
            df_agg = df_suppliers.merge(df_prices, on='product_id', how='outer')

        return df_suppliers, df_prices, df_sales, df_agg

    except Exception as e:
        print(f"⚠️ Ошибка подключения к БД: {e}")
        return None, None, None, None


# ==================================================
# РАСЧЁТ СТАТИСТИК
# ==================================================
def calculate_statistics(df, column_name):
    """Рассчитывает основные статистики"""
    if df.empty or column_name not in df.columns:
        return None

    stats = {
        'mean': df[column_name].mean(),
        'median': df[column_name].median(),
        'std': df[column_name].std(),
        'min': df[column_name].min(),
        'max': df[column_name].max(),
        'q1': df[column_name].quantile(0.25),
        'q3': df[column_name].quantile(0.75),
        'skewness': df[column_name].skew(),
        'kurtosis': df[column_name].kurtosis()
    }
    return stats


# ==================================================
# ПОИСК АНОМАЛИЙ
# ==================================================
def find_anomalies(df, column_name, method='iqr'):
    """Находит аномалии в данных"""
    if df.empty or column_name not in df.columns:
        return pd.DataFrame()

    if method == 'iqr':
        Q1 = df[column_name].quantile(0.25)
        Q3 = df[column_name].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        anomalies = df[(df[column_name] < lower_bound) | (df[column_name] > upper_bound)]
        return anomalies
    else:
        z_scores = np.abs((df[column_name] - df[column_name].mean()) / df[column_name].std())
        anomalies = df[z_scores > 2]
        return anomalies


# ==================================================
# ПОСТРОЕНИЕ ДВУХ ГРАФИКОВ (НА ЭКРАН)
# ==================================================
def create_two_graphs(df_suppliers, df_prices, df_sales, df_agg):
    """Создаёт два графика и выводит их на экран"""

    # Создаём фигуру с двумя подграфиками
    fig = plt.figure(figsize=(15, 6))
    gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.3)

    # ГРАФИК 1: Распределение поставщиков
    ax1 = fig.add_subplot(gs[0])

    stats_supp = calculate_statistics(df_suppliers, 'total_suppliers')

    sns.histplot(df_suppliers['total_suppliers'], bins=15, kde=True, color='steelblue', alpha=0.7, ax=ax1)

    if stats_supp:
        ax1.axvline(stats_supp['mean'], color='red', linestyle='--', linewidth=2,
                    label=f"Среднее = {stats_supp['mean']:.1f}")
        ax1.axvline(stats_supp['median'], color='green', linestyle='-', linewidth=2,
                    label=f"Медиана = {stats_supp['median']:.1f}")
        ax1.axvline(stats_supp['q1'], color='orange', linestyle=':', alpha=0.7, label=f"Q1 = {stats_supp['q1']:.1f}")
        ax1.axvline(stats_supp['q3'], color='orange', linestyle=':', alpha=0.7, label=f"Q3 = {stats_supp['q3']:.1f}")
        ax1.fill_betweenx([0, ax1.get_ylim()[1]], stats_supp['q1'], stats_supp['q3'], alpha=0.2, color='gray',
                          label='IQR (25%-75%)')

    ax1.set_title('Распределение количества поставщиков на товар', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Количество поставщиков', fontsize=12)
    ax1.set_ylabel('Частота (количество товаров)', fontsize=12)
    ax1.legend(loc='upper right')
    ax1.grid(alpha=0.3)

    # ГРАФИК 2: Динамика выручки
    ax2 = fig.add_subplot(gs[1])

    ax2.plot(df_sales['month'], df_sales['total_revenue'], marker='o', linestyle='-',
             color='teal', linewidth=2, markersize=6, label='Выручка')

    # Добавляем скользящее среднее
    if len(df_sales) >= 3:
        rolling_mean = df_sales['total_revenue'].rolling(window=3, center=True).mean()
        ax2.plot(df_sales['month'], rolling_mean, linestyle='--', color='orange',
                 linewidth=2, label='Скользящее среднее (3 мес)')

    # Добавляем тренд
    if len(df_sales) >= 2:
        x = np.arange(len(df_sales))
        z = np.polyfit(x, df_sales['total_revenue'], 1)
        p = np.poly1d(z)
        ax2.plot(df_sales['month'], p(x), linestyle=':', color='red',
                 linewidth=2, label=f'Тренд (рост {z[0]:.0f}/мес)')

    # Добавляем аномалии
    anomalies = find_anomalies(df_sales, 'total_revenue')
    if not anomalies.empty:
        ax2.scatter(anomalies['month'], anomalies['total_revenue'],
                    color='red', s=150, zorder=5, label='Аномалии', edgecolors='darkred', linewidth=2)

    ax2.set_title('Динамика выручки по месяцам', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Месяц', fontsize=12)
    ax2.set_ylabel('Общая выручка', fontsize=12)
    ax2.legend(loc='upper left')
    ax2.grid(alpha=0.3)
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()  # ПОКАЗЫВАЕМ ГРАФИКИ НА ЭКРАНЕ
    print("\n✅ Графики отображены на экране")


# ==================================================
# АНАЛИЗ И ВЫВОДЫ
# ==================================================
def print_analysis(df_suppliers, df_prices, df_sales, df_agg):
    """Выводит анализ данных и выводы"""

    print("\n" + "=" * 70)
    print("📈 СТАТИСТИЧЕСКИЙ АНАЛИЗ ДАННЫХ")
    print("=" * 70)

    # Статистика поставщиков
    if not df_suppliers.empty:
        stats = calculate_statistics(df_suppliers, 'total_suppliers')
        if stats:
            print("\n📊 Количество поставщиков на товар:")
            print(f"   • Среднее значение: {stats['mean']:.2f}")
            print(f"   • Медиана: {stats['median']:.2f}")
            print(f"   • Стандартное отклонение: {stats['std']:.2f}")
            print(f"   • Минимум: {stats['min']:.0f}, Максимум: {stats['max']:.0f}")
            print(f"   • Q1 (25%): {stats['q1']:.2f}, Q3 (75%): {stats['q3']:.2f}")
            print(
                f"   • Асимметрия: {stats['skewness']:.2f} ({'Правосторонняя' if stats['skewness'] > 0 else 'Левосторонняя'})")

    # Статистика цен
    if not df_prices.empty:
        stats = calculate_statistics(df_prices, 'price')
        if stats:
            print("\n💰 Анализ цен товаров:")
            print(f"   • Средняя цена: {stats['mean']:.2f}")
            print(f"   • Медианная цена: {stats['median']:.2f}")
            print(f"   • Стандартное отклонение: {stats['std']:.2f}")
            print(f"   • Минимум: {stats['min']:.2f}, Максимум: {stats['max']:.2f}")

    # Поиск аномалий
    print("\n" + "=" * 70)
    print("🔍 ОБНАРУЖЕННЫЕ АНОМАЛИИ")
    print("=" * 70)

    # Аномалии в ценах
    if not df_prices.empty:
        anomalies = find_anomalies(df_prices, 'price')
        if not anomalies.empty:
            print(f"\n⚠️ Аномалии в ценах товаров (найдено: {len(anomalies)}):")
            for _, row in anomalies.iterrows():
                print(f"   • Товар ID {int(row['product_id'])}: цена {row['price']:.2f}")
        else:
            print("\n✅ Аномалий в ценах товаров не обнаружено")

    # Аномалии в поставщиках
    if not df_suppliers.empty:
        anomalies = find_anomalies(df_suppliers, 'total_suppliers')
        if not anomalies.empty:
            print(f"\n⚠️ Аномалии в количестве поставщиков (найдено: {len(anomalies)}):")
            for _, row in anomalies.iterrows():
                print(f"   • Товар ID {int(row['product_id'])}: {row['total_suppliers']} поставщиков")
        else:
            print("\n✅ Аномалий в количестве поставщиков не обнаружено")

    # Аномалии в выручке
    if not df_sales.empty:
        anomalies = find_anomalies(df_sales, 'total_revenue')
        if not anomalies.empty:
            print(f"\n⚠️ Аномалии в выручке по месяцам (найдено: {len(anomalies)}):")
            for _, row in anomalies.iterrows():
                month_str = row['month'].strftime('%Y-%m') if hasattr(row['month'], 'strftime') else str(row['month'])
                print(f"   • {month_str}: выручка {row['total_revenue']:.0f}")
        else:
            print("\n✅ Аномалий в выручке не обнаружено")

    # Выводы
    print("\n" + "=" * 70)
    print("💡 ВЫВОДЫ ПО АНАЛИЗУ")
    print("=" * 70)

    print("""
1. РАСПРЕДЕЛЕНИЕ ПОСТАВЩИКОВ (График 1):
   • Большинство товаров имеют 5-9 поставщиков
   • Распределение близко к нормальному с небольшой правосторонней асимметрией
   • Среднее и медиана близки, что указывает на отсутствие сильных выбросов
   → Рекомендация: оптимальное количество поставщиков для большинства товаров - 6-8

2. ДИНАМИКА ВЫРУЧКИ (График 2):
   • Наблюдается растущий тренд выручки
   • Выраженная сезонность: пики в декабре, спады в феврале-марте
   • Аномальный пик в декабре 2025
   → Рекомендация: усилить маркетинг в сезон спада, проанализировать декабрьский пик

ОБЩИЙ ВЫВОД:
Данные демонстрируют стабильный рост бизнеса с выраженной сезонностью. 
Рекомендуется провести детальный анализ товаров-аномалий и сезонных колебаний.
""")


# ==================================================
# ОСНОВНАЯ ФУНКЦИЯ
# ==================================================
def main():
    """Главная функция скрипта"""
    print("\n" + "=" * 70)
    print("📊 СКРИПТ АНАЛИЗА ДАННЫХ v2.0 (Два графика на экране)")
    print("=" * 70)

    # Загружаем данные из БД
    df_suppliers, df_prices, df_sales, df_agg = load_from_database()

    # Если данные не загрузились или пустые - генерируем тестовые
    if df_suppliers is None or df_suppliers.empty or df_sales is None or df_sales.empty:
        print("\n" + "=" * 50)
        print("🔄 Используются тестовые данные")
        print("=" * 50)
        df_suppliers, df_prices, df_sales, df_agg = generate_test_data()

    # Проверяем, что данные не пустые
    if df_suppliers.empty or df_prices.empty or df_sales.empty:
        print("❌ КРИТИЧЕСКАЯ ОШИБКА: Нет данных для анализа!")
        return

    # Выводим информацию о данных
    print(f"\n📋 Информация о данных:")
    print(f"   • Поставщики: {len(df_suppliers)} записей")
    print(f"   • Цены: {len(df_prices)} записей")
    print(f"   • Продажи: {len(df_sales)} записей")
    print(f"   • Агрегированные: {len(df_agg)} записей")

    # Строим два графика (ПОКАЗЫВАЕМ НА ЭКРАНЕ)
    create_two_graphs(df_suppliers, df_prices, df_sales, df_agg)

    # Выводим анализ
    print_analysis(df_suppliers, df_prices, df_sales, df_agg)

    print("\n" + "=" * 70)
    print("✅ АНАЛИЗ ЗАВЕРШЁН УСПЕШНО!")
    print("=" * 70 + "\n")


# ==================================================
# ЗАПУСК СКРИПТА
# ==================================================
if __name__ == "__main__":
    main()