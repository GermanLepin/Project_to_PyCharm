import psycopg2

conn = psycopg2.connect(dbname="firstdb", user="postgres", password="********") # коннект к базе данных в моем случае это PostgreSQL
cur = conn.cursor()

cur.execute ("DROP TABLE IF EXISTS salary")
cur.execute ("DROP TABLE IF EXISTS traffic_light")
conn.commit()

cur.execute ("""CREATE TABLE salary
             (worker_id serial PRIMARY KEY, 
             first_name varchar,
             last_name varchar,
             salary int);""")

cur.execute("""INSERT INTO salary (first_name, last_name, salary) 
            VALUES (%s, %s, %s)""", ("Erick","Jonson", 2100)) #заливка данных в таблицу через timeplace(%s)
#BIG NO
#cur.execute("""INSERT INTO salary (first_name, last_name, salary)
#              VALUES (%s, %s, %s)""", % ("Erick","Jonson", 100))  это пример SQL инъекция (%,|| - так делать нельзя)

cur.execute("""
            INSERT INTO salary (first_name, last_name, salary)  
            VALUES (%(first_name)s, %(last_name)s, %(salary)s);
            """, {'first_name': 'Josef', 'last_name': 'Man', 'salary': 1800})

cur.execute("""
            INSERT INTO salary (first_name, last_name, salary)  
            VALUES (%(first_name)s, %(last_name)s, %(salary)s);
            """, {'first_name': 'Gabriel', 'last_name': 'Erlih', 'salary': 1950})
cur.execute("""
           INSERT INTO salary (first_name, last_name, salary)  
            VALUES (%(first_name)s, %(last_name)s, %(salary)s);
            """, {'first_name': 'Dynte', 'last_name': 'Samuel', 'salary': 1650})

conn.commit()

cur.execute ("""CREATE TABLE traffic_light 
            (light_id serial PRIMARY KEY, 
            light text);""")

#WRONG USAGE
#cur.execute ("INSER INTO traffic_light (light) VALUES('%s')", (10,)) нельзя заключать форматный плейсхолдеры в кавычки
#cur.execute ("INSER INTO traffic_light (light) VALUES('%d')", (10,)) нельзя заключать форматный плейсхолдеры в кавычки
#cur.execute ("INSER INTO traffic_light (light) VALUES('%d')", (10)) обязательно, даже если один аргумент передается в тюпле, должна быть запятая

cur.execute("INSERT INTO traffic_light(light) VALUES (%s)", ("red",))

cur.execute("SELECT * FROM salary") #данные находятся в cursor, что показать данные нужно выполнить функции fetchone для одной строки или fetchall для многих/всех запесей в БД
one_line = cur.fetchone()
print(one_line)

full_fetch = cur.fetchall()
for record in full_fetch:
    print(record)

full_fetch[0][0]

cur.execute("SELECT * FROM traffic_light")
full_fetch = cur.fetchall()
for record in full_fetch:
    print(record)

conn.commit()

cur.close()
conn.close()

conn = psycopg2.connect(dbname="firstdb", user="postgres", password="********")
with conn:
    with conn.cursor() as curs:
        curs.execute("""
                    UPDATE salary
                    SET salary = %s
                    WHERE first_name = %s
                    """, (1900, 'Erick'))

try:
    with conn:
        with conn.cursor() as curs:
            curs.execute("SELECT * FROM salary")
            print(curs.fetchall())
finally:
    conn.close()
