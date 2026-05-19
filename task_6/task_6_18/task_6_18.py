#№1

import psycopg2

import pandas as pd



try:

    
    connection = psycopg2.connect(

        host="localhost",         

        port="5435",              

        user="postgres",           

        password="student",       

        database="student_task"          

    )

    print("Можно работать дальше")



except Exception as error:

    print(f"Не выйдет из-зв ошибки: {error}")


#№2

query = """
SELECT prices.*, products.name AS product_name, products.category AS product_category
FROM prices
JOIN products ON prices.product_id = products.id
"""

minijoin = pd.read_sql_query(query, conn)

print(minijoin)

#№3

prices_df = pd.read_sql_query("SELECT price FROM prices", conn)

avg = prices_df['price'].mean()
mp = prices_df['price'].median()
std = prices_df['price'].std()
min = prices_df['price'].min()
max = prices_df['price'].max()

print(f"среднее значение: {avg:.2f} rub")
print(f"медианa: {mp:.2f} rub")
print(f"стандартное отклонение: {std:.2f} rub")
print(f"минимальнaя цена: {min:.2f} rub")
print(f"максимальная цена: {max:.2f} rub")

#№4

Q1 = prices_df['price'].quantile(0.25)
Q2 = prices_df['price'].quantile(0.5) 
Q3 = prices_df['price'].quantile(0.75)
IQR = Q3 - Q1
spisok = prices_df[prices_df['price'] > Q3]

print(f"первый квартиль: {Q1:.2f} rub")
print(f"второй квартиль, медиана: {Q2:.2f} rub")
print(f"третий квартиль: {Q3:.2f} rub")
print(f"межквартильный размах : {IQR:.2f} rub")
print("\n список товаров, цена которых превышает Q3:")
print(spisok[['product_name', 'product_category', 'price']].to_string(index=False))


#№3

new_prices_df = pd.read_sql_query(
    "SELECT prices.price, products.category \
     FROM prices JOIN products ON prices.product_id = products.id", 
    conn
)

grouped = new_prices_df.groupby('category').agg(
    count=('price', 'count'),
    new_avg=('price', 'mean'),
    new_mp=('price', 'median'),
    new_std=('price', 'std')
).reset_index()

sortirovka = grouped.sort_values(by='new_avg', ascending=False)

print(sortirovka)

#№6

new_new_prices_df = pd.read_sql_query(
    "SELECT prices.price, products.name AS product_name \
     FROM prices JOIN products ON prices.product_id = products.id", 
    conn
)

conn.close()

price_range = prices_df.groupby('product_name').agg(
    new_min=('price', 'min'),
    new_max=('price', 'max')
).reset_index()

price_range['price_range'] = price_range['new_max'] - price_range['new_min']
top_5 = price_range.sort_values(by='price_range', ascending=False).head(5)

print(top_5[['product_name', 'min_price', 'max_price', 'price_range']])

