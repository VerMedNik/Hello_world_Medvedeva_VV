import psycopg2

connection = None
cursor = None

try:
    connection = psycopg2.connect(
        host="localhost",         
        port="5432",               
        user="postgres",           
        password="example",        
        database="testdb"          
    )
 cur = con.cursor()
    cur.execute("SELECT * FROM courses ORDER BY credits ASC LIMIT 5")
    result = cur.fetchall()
    print(result)
except Exception as error:
    print(f"Ошибка при подключении: {error}")