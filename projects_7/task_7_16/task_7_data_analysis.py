import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# ============================================================================
# БЛОК 1: ПОДКЛЮЧЕНИЕ К БАЗЕ ДАННЫХ
# ============================================================================

conn = psycopg2.connect(
    host="localhost",
    port="5433",
    user="postgres",
    password="example",
    database="testdb"
)
print("✓ Подключение установлено")

# Запрос 1: средний балл по курсам
df_courses = pd.read_sql("""
    SELECT
        c.course_name AS course,
        ROUND(AVG(e.grade)::numeric, 2) AS avg_grade,
        COUNT(e.enrollment_id) AS total_enrollments
    FROM enrollments e
    JOIN courses c ON e.course_id = c.course_id
    GROUP BY c.course_name
    ORDER BY avg_grade DESC
""", conn)

# Запрос 2: все оценки
df_grades = pd.read_sql("SELECT grade FROM enrollments", conn)

# Запрос 3: студенты без оценок (аномалия)
df_missing = pd.read_sql("""
    SELECT COUNT(*) as missing_count
    FROM students s
    LEFT JOIN enrollments e ON s.student_id = e.student_id
    WHERE e.enrollment_id IS NULL
""", conn)

conn.close()
print("✓ Соединение закрыто\n")

# ============================================================================
# БЛОК 2: СТАТИСТИЧЕСКИЕ МЕТРИКИ
# ============================================================================

# Короткие названия
NAME_MAP = {
    "Основы программирования на Python": "Python",
    "Алгоритмы и структуры данных": "Алгоритмы",
    "Базы данных и SQL": "SQL",
    "Веб-разработка (Frontend)": "Frontend",
    "Администрирование Linux": "Linux",
    "Математический анализ": "Матанализ",
    "Дискретная математика": "Дискр. матем.",
    "Английский язык для IT": "Английский",
}
df_courses["short_name"] = df_courses["course"].map(NAME_MAP)

# Расчёт метрик
total_records = len(df_grades)
overall_avg = df_grades["grade"].mean()
overall_median = df_grades["grade"].median()
overall_std = df_grades["grade"].std()
grade_counts = df_grades["grade"].value_counts().sort_index()
missing_count = df_missing["missing_count"].iloc[0]
total_students = 40

print("=" * 60)
print("СТАТИСТИЧЕСКИЕ МЕТРИКИ")
print("=" * 60)
print(f"Всего студентов:                    {total_students}")
print(f"Студентов без оценок (аномалия):    {missing_count}")
print(f"Всего записей об оценках:           {total_records}")
print(f"Общий средний балл:                 {overall_avg:.2f}")
print(f"Медиана оценок:                     {overall_median:.1f}")
print(f"Стандартное отклонение:             {overall_std:.2f}")
print(f"Оценок 5:                           {grade_counts.get(5, 0)}")
print(f"Оценок 4:                           {grade_counts.get(4, 0)}")
print(f"Оценок 3:                           {grade_counts.get(3, 0)}")
print(f"Оценок 2:                           {grade_counts.get(2, 0)}")
print("\n" + "=" * 60)
print("СРЕДНИЙ БАЛЛ ПО КУРСАМ")
print("=" * 60)
for _, row in df_courses.iterrows():
    print(f"{row['short_name']:12} {row['avg_grade']:.2f}  ({row['total_enrollments']} сдач)")
print("=" * 60)

# ============================================================================
# БЛОК 3: ПОСТРОЕНИЕ ГРАФИКОВ
# ============================================================================

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Анализ успеваемости студентов", fontsize=14, fontweight="bold")

# ГРАФИК 1: Средний балл по курсам (горизонтальная столбчатая диаграмма)
colors = ["#d9534f" if g < overall_avg else "#4a90d9" for g in df_courses["avg_grade"]]
bars1 = ax1.barh(df_courses["short_name"], df_courses["avg_grade"],
                 color=colors, edgecolor="white", height=0.6)

for bar, val in zip(bars1, df_courses["avg_grade"]):
    ax1.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
             f"{val:.2f}", va="center", fontsize=9)

ax1.axvline(overall_avg, color="darkorange", linestyle="--", linewidth=1.5,
            label=f"Общее среднее: {overall_avg:.2f}")
ax1.set_xlim(2, 5.5)
ax1.set_xlabel("Средний балл")
ax1.set_title("График 1: Средний балл по курсам", fontweight="bold")

legend_patches = [
    Patch(facecolor="#4a90d9", label=f"Выше или равно среднему ({overall_avg:.2f})"),
    Patch(facecolor="#d9534f", label="Ниже среднего"),
]
ax1.legend(handles=legend_patches, fontsize=8, loc="lower right")

# ГРАФИК 2: Распределение оценок (гистограмма)
bars2 = ax2.bar(grade_counts.index, grade_counts.values, color="#f0ad4e",
                edgecolor="white", width=0.5)

for bar, (grade, cnt) in zip(bars2, grade_counts.items()):
    pct = cnt / total_records * 100
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             f"{cnt}\n({pct:.0f}%)", ha="center", fontsize=9)

ax2.axvline(overall_avg, color="blue", linestyle="--", linewidth=1.5,
            label=f"Среднее: {overall_avg:.2f}")
ax2.axvline(overall_median, color="green", linestyle=":", linewidth=1.5,
            label=f"Медиана: {overall_median:.0f}")

if grade_counts.get(2, 0) > 0:
    ax2.annotate(f"Аномалия:\n{grade_counts.get(2, 0)} двойки",
                 xy=(2, grade_counts.get(2, 0)),
                 xytext=(2.6, grade_counts.get(2, 0) + 3),
                 arrowprops={"arrowstyle": "->", "color": "red"},
                 fontsize=8, color="red")

ax2.set_xticks([2, 3, 4, 5])
ax2.set_xlabel("Оценка")
ax2.set_ylabel("Количество записей")
ax2.set_title("График 2: Распределение оценок", fontweight="bold")
ax2.legend(fontsize=8)

stats_box = (
    f"Статистика:\n"
    f"• Записей: {total_records}\n"
    f"• Среднее: {overall_avg:.2f}\n"
    f"• Медиана: {overall_median:.0f}\n"
    f"• Ст.откл.: {overall_std:.2f}"
)
ax2.text(0.97, 0.97, stats_box, transform=ax2.transAxes,
         va="top", ha="right", fontsize=8,
         bbox={"boxstyle": "round,pad=0.3", "facecolor": "lightyellow"})

plt.tight_layout()
plt.savefig("task_7_analysis_charts.png", dpi=150)
print("\n✓ График сохранён: task_7_analysis_charts.png")
plt.show()

# ============================================================================
# БЛОК 4: ВЫВОДЫ ПО ГРАФИКАМ
# ============================================================================

print("\n" + "=" * 60)
print("ВЫВОДЫ ПО ГРАФИКАМ")
print("=" * 60)

print("""
[ГРАФИК 1: Средний балл по курсам]

1. Лучшие курсы по успеваемости:
   - Английский язык для IT и Базы данных и SQL имеют наивысший средний балл (4.50)
   - Это может говорить о хорошей подаче материала или менее строгом оценивании

2. Проблемный курс:
   - Администрирование Linux (3.60) - единственный курс со средним баллом ниже 4.0
   - Требует внимания преподавателя и возможного пересмотра методики

3. Основная масса курсов держится на уровне 4.0-4.2, что является хорошим показателем

[ГРАФИК 2: Распределение оценок]

1. Статистика успеваемости:
   - Средний балл: 4.00
   - Медиана: 4.0
   - Стандартное отклонение: 0.82 (разброс оценок умеренный)

2. Частота оценок:
   - Оценка "4" - самая частая (53% от всех оценок)
   - Оценка "5" - 24% (каждый четвертый студент сдал на отлично)
   - Оценка "3" - 20%
   - Оценка "2" - всего 4% (редкие выбросы)

3. Общий вывод:
   - Распределение сдвинуто в сторону высоких оценок (положительная динамика)
   - Большинство студентов успешно осваивают программу
""")

print("=" * 60)
print("ОБНАРУЖЕННЫЕ АНОМАЛИИ")
print("=" * 60)

print(f"""
1. КРИТИЧЕСКАЯ АНОМАЛИЯ: отсутствие записей об успеваемости
   - {missing_count} из {total_students} студентов ({missing_count/total_students*100:.0f}%) 
     не имеют ни одной оценки в таблице enrollments
   - Возможные причины: ошибка при заполнении БД или студенты ещё не сдавали экзамены
   - Рекомендация: проверить процесс загрузки данных

2. СТАТИСТИЧЕСКАЯ АНОМАЛИЯ: редкие оценки "2"
   - {grade_counts.get(2, 0)} двойки из {total_records} записей ({grade_counts.get(2, 0)/total_records*100:.1f}%)
   - Являются выбросами на фоне общего распределения
   - Рекомендация: проверить конкретных студентов и причины получения двоек
""")

print("=" * 60)
print("ВЫПОЛНЕНИЕ ЗАВЕРШЕНО")
print("=" * 60)