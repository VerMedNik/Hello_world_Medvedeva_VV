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
    print("Все работает")

    df_products = pd.read_sql("""
        SELECT
            name,
            category,
            prices,
            suppliers
        FROM products
    """, connection)

    df_suppliers = df_products.groupby('category')['suppliers'].nunique().reset_index()
    df_suppliers.rename(columns={'suppliers': 'total_suppliers'}, inplace=True)
    df_categories = df_products['category'].value_counts().reset_index()
    df_categories.columns = ['category', 'count']
    df_prices = df_products[['name', 'prices', 'category']]

except Exception as error:
    print(f"Ошибка: {error}")
    raise SystemExit

 
connection.close()

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

fig = plt.figure(figsize=(16, 10))
fig.suptitle("Анализ данных о продуктах", fontsize=15, fontweight="bold", y=1.01)

gs = gridspec.GridSpec(2, 3, figure=fig,
                   height_ratios=[5, 4],
                   width_ratios=[2, 1, 2],
                   hspace=0.45, wspace=0.35)

ax1 = fig.add_subplot(gs[0, 0:2])
ax2 = fig.add_subplot(gs[0, 2])
ax3 = fig.add_subplot(gs[1, 0])
ax4 = fig.add_subplot(gs[1, 1:3])

# 1
avg_price_by_category = df_products.groupby('category')['price'].mean().round(2)
categories = avg_price_by_category.index
avg_prices = avg_price_by_category.values

bars1 = ax1.barh(
    categories,
    avg_prices,
    color="#4a90d9",
    edgecolor="white",
    height=0.6
)
for bar, val in zip(bars1, avg_prices):
    ax1.text(
        bar.get_width() + 0.04,
        bar.get_y() + bar.get_height() / 2,
        f"{val:.2f}",
        va="center", fontsize=9,
    )

overall_avg_price = df_products['price'].mean()
ax1.axvline(overall_avg_price, color="darkorange", linestyle="--",
            linewidth=1.3, label=f"Среднее: {overall_avg_price:.2f}")

ax1.set_xlim(0, max(avg_prices) * 1.2)
ax1.set_xlabel("Средняя цена, руб.")
ax1.set_title("Средняя цена по категориям товаров", fontweight="bold", pad=8)
ax1.legend(fontsize=8, loc="lower right")


# 2
supplier_counts = df_products['suppliers'].value_counts()
suppliers = supplier_counts.index
counts = supplier_counts.values

bars2 = ax2.bar(
    suppliers,
    counts,
    color="#5cb85c",
    edgecolor="white",
    width=0.6
)

for bar in bars2:
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.15,
        str(int(bar.get_height())),
        ha="center", fontsize=9,
    )

ax2.set_ylim(0, max(counts) + 2.5)
ax2.set_ylabel("Количество товаров")
ax2.set_title("Количество товаров\nпо поставщикам", fontweight="bold", pad=8)

ax2.set_xticks(range(len(suppliers)))
ax2.set_xticklabels(suppliers, rotation=40, ha="right", fontsize=8)

# 3
category_counts = df_products['category'].value_counts()
categories_pie = category_counts.index
values_pie = category_counts.values

pie_labels = [f"{cat} ({val} шт.)" for cat, val in zip(categories_pie, values_pie)]

pie_colors = ["#7b68ee", "#4a90d9", "#2ecc71", "#f0ad4e", "#d9534f"]

wedges, texts, autotexts = ax3.pie(
    values_pie,
    labels=None,
    autopct="%1.0f%%",
    colors=pie_colors,
    startangle=90,
    wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    pctdistance=0.7
)

for autotext in autotexts:
    autotext.set_fontsize(10)
    autotext.set_fontweight("bold")

ax3.set_title("Распределение товаров\nпо категориям", fontweight="bold", pad=8)

ax3.legend(
    wedges, pie_labels,
    loc="lower center",
    bbox_to_anchor=(0.5, -0.22),
    fontsize=8,
    frameon=False,
)

#4
data_for_boxplot = [
    df_products[df_products['category'] == cat]['price'].values
    for cat in categories
]

boxplot = ax4.boxplot(
    data_for_boxplot,
    labels=categories,
    patch_artist=True,
    medianprops={'color': 'red', 'linewidth': 2},
    boxprops={'facecolor': '#4a90d9', 'alpha': 0.7}
)

ax4.set_xlabel("Категория товара")
ax4.set_ylabel("Цена, руб.")
ax4.set_title("Распределение цен по категориям товаров", fontweight="bold", pad=8)

ax4.tick_params(axis='x', rotation=45)

stats_text = (
    f"Всего товаров: {len(df_products)}\n"
    f"Средняя цена: {df_products['price'].mean():.2f} руб.\n"
    f"Мин. цена: {df_products['price'].min():.2f} руб.\n"
    f"Макс. цена: {df_products['price'].max():.2f} руб."
)

ax4.text(0.97, 0.95, stats_text,
         transform=ax4.transAxes,
         va="top", ha="right", fontsize=8,
         bbox={"boxstyle": "round,pad=0.4", "facecolor": "lightyellow",
              "edgecolor": "lightgray", "alpha": 0.8})


price_std = df_products['price'].std()
price_mean = df_products['price'].mean()
outliers_high = df_products[df_products['price'] > price_mean + 2 * price_std]
outliers_low = df_products[df_products['price'] < price_mean - 2 * price_std]

if not outliers_high.empty:
    ax4.annotate(
        f"Аномально высокие цены:\n{len(outliers_high)} товаров",
        xy=(1, price_mean + 2 * price_std),
        xytext=(1.2, price_mean + 3 * price_std),
        arrowprops={"arrowstyle": "->", "color": "crimson"},
        fontsize=8, color="crimson",
    )

if not outliers_low.empty:
    ax4.annotate(
        f"Аномально низкие цены:\n{len(outliers_low)} товаров",
        xy=(1, price_mean - 2 * price_std),
        xytext=(1.2, price_mean - 3 * price_std),
        arrowprops={"arrowstyle": "->", "color": "darkgreen"},
        fontsize=8, color="darkgreen",
    )

#ctr+s

OUTPUT_FILE = "products_analysis.png"

plt.savefig(OUTPUT_FILE, bbox_inches="tight", dpi=150)
print(f"✓ График сохранён: {OUTPUT_FILE}")

plt.show()