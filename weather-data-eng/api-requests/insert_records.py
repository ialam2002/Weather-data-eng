from api_requests import fetch_data, mock_data
import psycopg2
def connect_to_database():
    print("Connecting to the database...")
    # Simulate a database connection
    try:
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            dbname='db',
            user='db_user',
            password='db_password'
        )
        print(conn)
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        raise

def create_table(conn):
    print("Creating table if not exist...")
    try:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE SCHEMA IF NOT EXISTS dev;
        CREATE TABLE IF NOT EXISTS dev.raw_weather_data (
        id SERIAL PRIMARY KEY,
        city TEXT,
        temperature FLOAT,
        weather_descriptions TEXT,
        wind_speed FLOAT,
        time TIMESTAMP,
        inserted_at TIMESTAMP DEFAULT NOW()
        utc_offset TEXT); """)
        conn.commit()
        print("Table created successfully")
    except psycopg2.Error as e:
        print(f"Error creating table: {e}")
        raise

def insert_data(conn, data):
    print("Inserting weather data into database...")
    try:
        cursor = conn.cursor()
        cursor.execute("""
                    INSERT INTO dev.raw_weather_data (city, temperature, weather_descriptions, wind_speed, time, utc_offset)
                       VALUES (%s, %s, %s, %s, %s, NOW(), %s ), (
                       location['name'],
                       weather['temperature'],
                       weather['weather_descriptions'][0],
                       weather['wind_speed'],
                       locataion['localtime'],
                       location['utc_offset'])
                       """)
        conn.commit()
        print("Data inserted successfully")
    except psycopg2.Error as e:
        print(f"Error inserting data: {e}")
        raise

def main():
    try:
        data = insert_data()
        conn = connect_to_database()
        create_table(conn)
        insert_data(conn, data)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn in locals():
            conn.close()
            print("Database connection closed.")

main()