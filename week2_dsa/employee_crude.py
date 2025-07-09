import pymysql

def connectDB():
    connection = None
    try:
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="udithsimha05",
            database="simhaudith_db",
            port=3306,
            charset="utf8",
            autocommit=True  # optional, so you don't have to call commit explicitly
        )
        print('Database Connected')
    except pymysql.MySQLError as e:
        print(f'Database Connection Failed: {e}')
    return connection

def disconnect_db(connection):
    if connection:
        try:
            connection.close()
            print('DB disconnected')
        except pymysql.MySQLError as e:
            print(f'DB disconnection failed: {e}')
    else:
        print('No connection to close')

def create_db():
    query = 'CREATE DATABASE IF NOT EXISTS simhaudith_db'
    connection = connectDB()
    if not connection:
        print('Cannot create database without connection')
        return
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            print('Database created or already exists')
    except pymysql.MySQLError as e:
        print(f'Database creation failed: {e}')
    finally:
        disconnect_db(connection)

def create_table():
    query = '''
    CREATE TABLE IF NOT EXISTS employees(
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(50) NOT NULL,
        designation VARCHAR(30),
        phone_number BIGINT UNIQUE,
        salary FLOAT,
        commission FLOAT DEFAULT 0,
        years_of_experience TINYINT,
        technology VARCHAR(30) NOT NULL
    )
    '''
    connection = connectDB()
    if not connection:
        print('Cannot create table without connection')
        return
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            print('Table created or already exists')
    except pymysql.MySQLError as e:
        print(f'Table creation failed: {e}')
    finally:
        disconnect_db(connection)

def read_all_employees():
    query = 'SELECT * FROM employees'
    connection = connectDB()
    if not connection:
        print('Cannot read employees without connection')
        return
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            print('All rows retrieved')
    except pymysql.MySQLError as e:
        print(f'Rows retrieval failed: {e}')
    finally:
        disconnect_db(connection)

# Example usage:
#create_db()  # call once if needed
create_table()
read_all_employees()