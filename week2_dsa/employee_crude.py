import pymysql

def connect_db():
    connection = None
    try:
        connection = pymysql.connect(
            host='localhost',
            user="root",
            password="udithsimha05",
            database='udithsimha_db',
            port=3306,
            charset="utf8"
        )
        print('Database Connected')
    except Exception as e:
        print(f'Database Connection Failed: {e}')
    return connection

def disconnect_db(connection):
    try:
        if connection:
            connection.close()
            print('DB disconnected')
        else:
            print('No connection to disconnect')
    except Exception as e:
        print(f'DB disconnection failed: {e}')

def create_db():
    query = 'CREATE DATABASE IF NOT EXISTS nithin_db'
    connection = connect_db()
    if connection is None:
        print('Cannot create database because connection failed')
        return
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        print('Database created')
        cursor.close()
        disconnect_db(connection)
    except Exception as e:
        print(f'Database creation failed: {e}')
        disconnect_db(connection)

def create_table():
    query = '''
    CREATE TABLE IF NOT EXISTS employees (
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
    connection = connect_db()
    if connection is None:
        print('Cannot create table because connection failed')
        return
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        print('Table created')
        cursor.close()
        disconnect_db(connection)
    except Exception as e:
        print(f'Table creation failed: {e}')
        disconnect_db(connection)

def read_all_employees():
    query = 'SELECT * FROM employees'
    connection = connect_db()
    if connection is None:
        print('Cannot retrieve employees because connection failed')
        return
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        print('All rows retrieved')
        cursor.close()
        disconnect_db(connection)
    except Exception as e:
        print(f'Rows retrieval failed: {e}')
        disconnect_db(connection)

# Usage example
create_table()
read_all_employees()

