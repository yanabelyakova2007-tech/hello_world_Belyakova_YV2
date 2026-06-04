"""
Веб-приложение для анализа базы данных student_task
Использует Flask, PostgreSQL, pandas, matplotlib
"""

import os
import io
import base64
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template, jsonify, send_file
from sqlalchemy import create_engine, text

# Настройка matplotlib для корректного отображения русских букв
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# ==================================================
# НАСТРОЙКА ПОДКЛЮЧЕНИЯ К БАЗЕ ДАННЫХ
# ==================================================
# ВАЖНО: замените параметры подключения на свои!
# Пример: postgresql://пользователь:пароль@localhost:5432/student_task

DB_USER = "postgres"  # ваш пользователь PostgreSQL
DB_PASSWORD = "example"  # ваш пароль
DB_HOST = "localhost"
DB_PORT = "5433"
DB_NAME = "testdb"

# Создаём строку подключения
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Создаём engine для SQLAlchemy (рекомендованный способ для pandas 2.x)
engine = create_engine(DATABASE_URL)

# Проверка подключения (опционально)
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ Подключение к базе данных успешно!")
except Exception as e:
    print(f"❌ Ошибка подключения к БД: {e}")

# ==================================================
# СОЗДАНИЕ ПРИЛОЖЕНИЯ FLASK
# ==================================================
app = Flask(__name__)


# ==================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ==================================================

def get_student_data() -> pd.DataFrame:
    """
    Загружает данные об успеваемости студентов из БД.
    Возвращает DataFrame с колонками: student_id, course, grade
    """
    query = """
        SELECT 
            s.id AS student_id,
            s.name AS student_name,
            c.name AS course,
            e.grade
        FROM enrollment e
        JOIN student s ON e.student_id = s.id
        JOIN course c ON e.course_id = c.id
        WHERE e.grade IS NOT NULL
    """
    return pd.read_sql(query, engine)


def get_course_stats() -> pd.DataFrame:
    """
    Загружает средние оценки по курсам.
    Возвращает DataFrame с колонками: course, avg_grade
    """
    query = """
        SELECT 
            c.name AS course,
            AVG(e.grade) AS avg_grade
        FROM enrollment e
        JOIN course c ON e.course_id = c.id
        WHERE e.grade IS NOT NULL
        GROUP BY c.name
        ORDER BY avg_grade DESC
    """
    return pd.read_sql(query, engine)


def get_grade_distribution() -> pd.DataFrame:
    """
    Загружает распределение оценок.
    Возвращает DataFrame с колонками: grade, count
    """
    query = """
        SELECT 
            grade,
            COUNT(*) AS count
        FROM enrollment
        WHERE grade IS NOT NULL
        GROUP BY grade
        ORDER BY grade
    """
    return pd.read_sql(query, engine)


# ==================================================
# МАРШРУТЫ (ROUTES) — ЭНДПОИНТЫ
# ==================================================

@app.route('/')
def index():
    """Главная страница — возвращает HTML-шаблон"""
    return render_template('index.html')


# ------------------- МАРШРУТЫ СТАТИСТИКИ -------------------
# Используем нейтральные имена, чтобы не блокировались адблокерами

@app.route('/api/metric/mean')
def api_mean():
    """Средняя оценка всех студентов"""
    try:
        df = get_student_data()
        mean_value = df['grade'].mean()
        return jsonify({
            'success': True,
            'value': round(mean_value, 2),
            'label': 'Средняя оценка',
            'description': 'Среднее арифметическое всех оценок'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/metric/median')
def api_median():
    """Медианная оценка всех студентов"""
    try:
        df = get_student_data()
        median_value = df['grade'].median()
        return jsonify({
            'success': True,
            'value': round(median_value, 2),
            'label': 'Медианная оценка',
            'description': 'Центральное значение: 50% оценок выше, 50% ниже'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/metric/total')
def api_total():
    """Общее количество оценок"""
    try:
        df = get_student_data()
        total_value = len(df)
        return jsonify({
            'success': True,
            'value': total_value,
            'label': 'Всего оценок',
            'description': f'Количество записей об успеваемости в базе'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/metric/std')
def api_std():
    """Стандартное отклонение оценок"""
    try:
        df = get_student_data()
        std_value = df['grade'].std()
        return jsonify({
            'success': True,
            'value': round(std_value, 2),
            'label': 'Стандартное отклонение',
            'description': 'Разброс оценок относительно среднего'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/metric/min')
def api_min():
    try:
        df = get_student_data()
        if df.empty:
            return jsonify({'success': False, 'error': 'Нет данных в таблице'}), 500
        min_value = df['grade'].min()
        return jsonify({
            'success': True,
            'value': float(min_value) if not pd.isna(min_value) else None,
            'label': 'Минимальная оценка',
            'description': 'Самая низкая оценка среди всех студентов'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/metric/max')
def api_max():
    try:
        df = get_student_data()
        if df.empty:
            return jsonify({'success': False, 'error': 'Нет данных в таблице'}), 500
        max_value = df['grade'].max()
        return jsonify({
            'success': True,
            'value': float(max_value) if not pd.isna(max_value) else None,
            'label': 'Максимальная оценка',
            'description': 'Самая высокая оценка среди всех студентов'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ------------------- МАРШРУТЫ ГРАФИКОВ -------------------

@app.route('/api/chart/histogram')
def api_histogram():
    """Гистограмма распределения оценок с отмеченной медианой"""
    try:
        df = get_student_data()
        grades = df['grade']

        # Считаем статистику
        mean_val = grades.mean()
        median_val = grades.median()

        # Создаём фигуру
        fig, ax = plt.subplots(figsize=(10, 6))

        # Рисуем гистограмму
        ax.hist(grades, bins=10, color='#2A9D8F', edgecolor='white', alpha=0.7)

        # Добавляем вертикальные линии для статистик
        ax.axvline(mean_val, color='blue', linestyle='--', linewidth=2,
                   label=f'Среднее = {mean_val:.2f}')
        ax.axvline(median_val, color='red', linestyle='-.', linewidth=2,
                   label=f'Медиана = {median_val:.2f}')

        # Настройка графика
        ax.set_xlabel('Оценка', fontsize=12)
        ax.set_ylabel('Количество студентов', fontsize=12)
        ax.set_title('Распределение оценок студентов', fontsize=14, fontweight='bold')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)

        # Сохраняем в PNG и кодируем в base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)

        return jsonify({
            'success': True,
            'image': img_base64,
            'stats': {
                'mean': round(mean_val, 2),
                'median': round(median_val, 2),
                'count': len(grades)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/chart/courses')
def api_courses_chart():
    """Столбчатая диаграмма средних баллов по курсам"""
    try:
        df = get_course_stats()

        # Считаем общее среднее для линии
        overall_mean = df['avg_grade'].mean()

        # Создаём фигуру
        fig, ax = plt.subplots(figsize=(10, 6))

        # Рисуем столбцы
        bars = ax.bar(df['course'], df['avg_grade'], color='#2A9D8F', alpha=0.7)

        # Добавляем горизонтальную линию общего среднего
        ax.axhline(overall_mean, color='red', linestyle='--', linewidth=2,
                   label=f'Общее среднее = {overall_mean:.2f}')

        # Подписываем значения на столбцах
        for bar, val in zip(bars, df['avg_grade']):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                    f'{val:.2f}', ha='center', va='bottom', fontsize=9)

        # Настройка графика
        ax.set_xlabel('Курс', fontsize=12)
        ax.set_ylabel('Средний балл', fontsize=12)
        ax.set_title('Средний балл по курсам', fontsize=14, fontweight='bold')
        ax.legend(loc='upper right')
        plt.xticks(rotation=45, ha='right')
        ax.grid(True, alpha=0.3, axis='y')

        # Сохраняем в PNG и кодируем в base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)

        return jsonify({
            'success': True,
            'image': img_base64,
            'stats': {
                'overall_mean': round(overall_mean, 2),
                'count_courses': len(df)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================================================
# ЗАПУСК ПРИЛОЖЕНИЯ
# ==================================================
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)