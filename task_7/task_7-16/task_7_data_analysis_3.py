import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch

try:
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        user="postgres",
        password="example",
        database="testdb"
    )

    print("✓ Подключение установлено")

    # График 1: средний балл по годам
    df_avg_grade_by_year = pd.read_sql("""
        SELECT
            s.enrollment_year AS year,
            ROUND(AVG(e.grade)::numeric, 2) AS avg_grade
        FROM enrollments e
        JOIN students s ON e.student_id = s.student_id
        GROUP BY s.enrollment_year
        ORDER BY s.enrollment_year
    """, connection)

    # График 2: количество сдач по годам
    df_enrollments_by_year = pd.read_sql("""
        SELECT
            s.enrollment_year AS year,
            COUNT(e.enrollment_id) AS total_enrollments
        FROM enrollments e
        JOIN students s ON e.student_id = s.student_id
        GROUP BY s.enrollment_year
        ORDER BY s.enrollment_year
    """, connection)

    # График 3: процент оценок из всех
    df_all_grades = pd.read_sql("SELECT grade FROM enrollments", connection)
    grade_percentages = df_all_grades['grade'].value_counts(normalize=True) * 100

    # График 4: распределение оценок по курсам
    df_grade_distribution_by_course = pd.read_sql("""
        SELECT
            c.course_name AS course,
            e.grade,
            COUNT(*) AS count
        FROM enrollments e
        JOIN courses c ON e.course_id = c.course_id
        GROUP BY c.course_name, e.grade
        ORDER BY c.course_name, e.grade
    """, connection)

    # Получаем количество студентов без оценок ДО закрытия соединения
    missing_students_count = pd.read_sql("""
        SELECT COUNT(*) AS count
        FROM students s
        LEFT JOIN enrollments e ON s.student_id = e.student_id
        WHERE e.enrollment_id IS NULL
    """, connection).iloc[0, 0]

    print(f"Записей среднего балла по годам: {len(df_avg_grade_by_year)}")
    print(f"Записей количества сдач по годам: {len(df_enrollments_by_year)}")
    print(f"Всего оценок: {len(df_all_grades)}")
    print(f"Записей распределения оценок по курсам: {len(df_grade_distribution_by_course)}")
    print(f"Студентов без оценок: {missing_students_count}")

except Exception as error:
    print(f"Ошибка подключения: {error}")
    raise SystemExit

finally:
    if connection:
        connection.close()
    print("✓ Соединение закрыто\n")

NAME_MAP = {
    "Основы программирования на Python": "Python",
    "Алгоритмы и структуры данных": "Алгоритмы",
    "Базы данных и SQL": "Базы данных",
    "Веб-разработка (Frontend)": "Frontend",
    "Администрирование Linux": "Linux",
    "Математический анализ": "Матанализ",
    "Дискретная математика": "Дискр. мат.",
    "Английский язык для IT": "Английский",
}

GRADE_THRESHOLD = 3.8

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linestyle": "--",
    "figure.dpi": 130,
})

fig = plt.figure(figsize=(16, 12))
fig.suptitle("Анализ учебной базы данных", fontsize=15, fontweight="bold", y=1.01)

gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.4, wspace=0.3)

ax1 = fig.add_subplot(gs[0, 0])  # График 1
ax2 = fig.add_subplot(gs[0, 1])  # График 2
ax3 = fig.add_subplot(gs[1, 0])  # График 3
ax4 = fig.add_subplot(gs[1, 1])  # График 4

# График 1: средний балл по годам (с нормой 3.8)
bars1 = ax1.bar(
    df_avg_grade_by_year["year"],
    df_avg_grade_by_year["avg_grade"],
    color=["#4a90d9" if g >= GRADE_THRESHOLD else "#e9c600" for g in df_avg_grade_by_year["avg_grade"]],
    edgecolor="white",
    width=0.6
)

for bar, val in zip(bars1, df_avg_grade_by_year["avg_grade"]):
    ax1.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.02,
        f"{val:.2f}",
        ha="center", fontsize=9
    )

ax1.axhline(GRADE_THRESHOLD, color="darkorange", linestyle="--",
           linewidth=1.3, label=f"Норма: {GRADE_THRESHOLD}")
ax1.set_ylim(2, 5.2)
ax1.set_xlabel("Год набора")
ax1.set_ylabel("Средний балл")
ax1.set_title("Средний балл по годам", fontweight="bold", pad=8)
ax1.legend(fontsize=8, loc="lower right")


# График 2: количество сдач по годам
bars2 = ax2.bar(
    df_enrollments_by_year["year"],
    df_enrollments_by_year["total_enrollments"],
    color="#7c5cb8",
    edgecolor="white",
    width=0.6
)

for bar in bars2:
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.15,
        str(int(bar.get_height())),
        ha="center", fontsize=9
    )

ax2.set_ylabel("Количество сдач")
ax2.set_xlabel("Год набора")
ax2.set_title("Количество сдач по годам", fontweight="bold", pad=8)

# График 3: процент оценок из всех
wedges, texts, autotexts = ax3.pie(
    grade_percentages.values,
    labels=[f"Оценка {g}" for g in grade_percentages.index],
    autopct="%1.1f%%",
    colors=["#6bd94f", "#f0ad4e", "#5c81b8", "#ce1818"],
    startangle=90,
    wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    pctdistance=0.7
)

for autotext in autotexts:
    autotext.set_fontsize(9)
    autotext.set_fontweight("bold")

ax3.set_title("Процент оценок из всех", fontweight="bold", pad=8)

# График 4: распределение оценок по курсам
pivot_data = df_grade_distribution_by_course.pivot(
    index="course", columns="grade", values="count"
).fillna(0)

# Приводим названия курсов к коротким через NAME_MAP
# Если соответствия нет, оставляем оригинальное название курса
pivot_data.index = pivot_data.index.map(lambda x: NAME_MAP.get(x, x))

# Сортируем курсы по сумме всех оценок (от большего к меньшему) для лучшей читаемости
pivot_data = pivot_data.loc[pivot_data.sum(axis=1).sort_values(ascending=False).index]

# Строим столбчатую диаграмму с накоплением
pivot_plot = pivot_data.plot(
    kind="bar",
    stacked=True,
    ax=ax4,
    color=["#d9534f", "#4e74f0", "#d3d60a", "#56d94a"],
    edgecolor="white",
    width=0.7
)

# Добавляем подписи значений на столбцы
for container in pivot_plot.containers:
    ax4.bar_label(
        container,
        label_type='center',
        fmt='%d',
        fontsize=8,
        color='white',
        fontweight='bold'
    )

ax4.set_xlabel("Курс", fontsize=10)
ax4.set_ylabel("Количество оценок", fontsize=10)
ax4.set_title("Распределение оценок по курсам", fontweight="bold", pad=8)
ax4.tick_params(axis="x", rotation=45, labelsize=9)
ax4.legend(
    title="Оценки",
    labels=["2", "3", "4", "5"],
    fontsize=8,
    loc="upper right"
)

# Улучшаем внешний вид: добавляем сетку по оси Y
ax4.grid(axis='y', alpha=0.3, linestyle='--')
ax4.set_axisbelow(True)  # Сетка под столбцами

# Общая статистика по всем данным для текстового блока
total_grades = len(df_all_grades)
avg_grade_overall = df_all_grades['grade'].mean()
median_grade = df_all_grades['grade'].median()
std_grade = df_all_grades['grade'].std()

stats_text = (
    f"Общая статистика:\n"
    f"Всего оценок: {total_grades}\n"
    f"Среднее: {avg_grade_overall:.2f}\n"
    f"Медиана: {median_grade}\n"
    f"Ст. откл.: {std_grade:.2f}\n"
    f"Норма: ≥{GRADE_THRESHOLD}"
)

# Добавляем блок с общей статистикой в правом верхнем углу
fig.text(
    0.95, 0.5,
    stats_text,
    transform=fig.transFigure,
    va="center",
    ha="right",
    fontsize=9,
    bbox={
        "boxstyle": "round,pad=0.4",
        "facecolor": "lightyellow",
        "edgecolor": "lightgray",
        "alpha": 0.8
    },
    zorder=10
)

# Подпись внизу графика с предупреждением о студентах без оценок
fig.text(
    0.5, -0.03,
    f"⚠ Внимание: {missing_students_count} студентов не имеют ни одной записи об успеваемости",
    ha="center",
    fontsize=9,
    color="#8b0000",
    bbox={
        "boxstyle": "round,pad=0.4",
        "facecolor": "#fff3f3",
        "edgecolor": "#d9534f"
    }
)

# Сохраняем график
OUTPUT_FILE = "student_charts_updated.png"
plt.savefig(OUTPUT_FILE, bbox_inches="tight", dpi=150, facecolor='white')
print(f"✓ График сохранён: {OUTPUT_FILE}")

plt.show()
