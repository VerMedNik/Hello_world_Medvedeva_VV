import pandas as pd

import matplotlib

matplotlib.use('Agg')  # ВАЖНО: серверный режим без GUI - см. ниже

import matplotlib.pyplot as plt

from io import BytesIO

from flask import Flask, render_template, jsonify, send_file

from sqlalchemy import create_engine



# --- Создаём Flask-приложение ---

app = Flask(__name__)

matplotlib.rcParams['font.family'] = 'DejaVu Sans'



# --- ENGINE создаётся ОДИН раз при запуске сервера ---

# Формат строки: postgresql+psycopg2://user:password@host:port/database

# SQLAlchemy сам управляет пулом соединений - нам не нужно вручную

# открывать/закрывать соединение в каждом маршруте.

ENGINE = create_engine(

    "postgresql+psycopg2://postgres:example@localhost:5432/testdb"

)





# =============================================================

#   МАРШРУТЫ

# =============================================================



# --- Главная страница: отдаёт index.html ---

@app.route("/")

def index():

    return render_template("index.html")





# --- API для статистики: /api/stat/mean, /api/stat/median, /api/stat/total ---

# ВНИМАНИЕ: НЕ используем слово "count" в URL - его блокируют

# многие адблокеры (uBlock Origin, AdBlock и встроенные). Берём "total".

@app.route("/api/stat/<metric>")

def get_stat(metric):

    try:

        # Передаём ENGINE напрямую - это то, чего ждёт pandas 2.x

        df = pd.read_sql("SELECT grade FROM enrollments", ENGINE)



        if metric == "mean":

            # f-строка с :.2f - всегда два знака после запятой ("4.16", "4.00")

            value = f"{df['grade'].mean():.2f}"

            label = "Средний балл"

        elif metric == "median":

            # Тоже два знака - иначе медиана "4.0" покажется без нулей

            value = f"{df['grade'].median():.2f}"

            label = "Медиана оценок"

        elif metric == "total":

            # Количество - целое число, форматирование не нужно

            value = int(df["grade"].count())

            label = "Всего записей"

        else:

            return jsonify({"error": "Неизвестная метрика"}), 400



        # jsonify(...) - превращает Python-словарь в JSON-ответ

        return jsonify({"label": label, "value": value})



    except Exception as e:

        # Печатаем ошибку в консоль - чтобы было видно, что пошло не так

        print(f"ERROR в /api/stat/{metric}: {e}")

        return jsonify({"error": str(e)}), 500





# --- API для графиков: /api/chart/histogram, /api/chart/courses ---

@app.route("/api/chart/<kind>")

def get_chart(kind):

    try:

        fig, ax = plt.subplots(figsize=(8, 5))



        if kind == "histogram":

            df = pd.read_sql("SELECT grade FROM enrollments", ENGINE)

            grade_counts = df["grade"].value_counts().sort_index()



            ax.bar(grade_counts.index, grade_counts.values,

                   color="#f0ad4e", edgecolor="white", width=0.5)



            # Статистическая метрика - медиана

            median = df["grade"].median()

            ax.axvline(median, color="crimson", linestyle="--",

                       linewidth=1.5, label=f"Медиана: {median}")



            ax.set_xlabel("Оценка")

            ax.set_ylabel("Количество записей")

            ax.set_title("Распределение оценок", fontweight="bold")

            ax.set_xticks([2, 3, 4, 5])

            ax.legend()



        elif kind == "courses":

            df = pd.read_sql("""

                SELECT c.course_name AS course,

                       ROUND(AVG(e.grade)::numeric, 2) AS avg_grade

                FROM enrollments e

                JOIN courses c ON e.course_id = c.course_id

                GROUP BY c.course_name

                ORDER BY avg_grade DESC

            """, ENGINE)



            # Сокращаем длинные названия для подписей

            short_names = df["course"].str[:12]



            ax.barh(short_names, df["avg_grade"],

                    color="#4a90d9", edgecolor="white")



            # --- Статистическая метрика: общее среднее по ВСЕМ оценкам ---

            # ВАЖНО: считаем именно по всем оценкам из enrollments, а не как

            # df["avg_grade"].mean() - "среднее по средним курсов". Это разные

            # числа! "Среднее по всем" учитывает, что в одних курсах много

            # студентов, а в других мало (взвешенное среднее).

            # "Среднее средних" игнорирует это и считает каждый курс одинаково

            # важным. Используем "среднее по всем", чтобы оно совпадало

            # со значением кнопки "Среднее".

            df_all = pd.read_sql("SELECT grade FROM enrollments", ENGINE)

            overall_avg = df_all["grade"].mean()



            ax.axvline(overall_avg, color="darkorange", linestyle="--",

                       linewidth=1.3, label=f"Среднее: {overall_avg:.2f}")



            ax.set_xlabel("Средний балл")

            ax.set_title("Средний балл по курсам", fontweight="bold")

            ax.set_xlim(0, 5.5)

            ax.legend(loc="lower right")



        else:

            plt.close(fig)

            return jsonify({"error": "Неизвестный тип графика"}), 400



        plt.tight_layout()



        # --- Главный приём: сохраняем PNG в память, не на диск ---

        buf = BytesIO()

        plt.savefig(buf, format="png", dpi=120, bbox_inches="tight")

        plt.close(fig)

        buf.seek(0)



        # send_file() - отправляет файл (или поток байтов) пользователю

        return send_file(buf, mimetype="image/png")



    except Exception as e:

        print(f"ERROR в /api/chart/{kind}: {e}")

        return jsonify({"error": str(e)}), 500





# --- Запуск приложения ---

if __name__ == "__main__":

   app.run(debug=True, port=5000)