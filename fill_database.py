import psycopg2
import os
from psycopg2 import Error
from dotenv import load_dotenv

load_dotenv()


def fill_airportcodes(codes):
    # Connect to your postgres DB

    try:
        conn = psycopg2.connect(user=os.getenv('user_db'),
                                password=os.getenv('password_db'),
                                host=os.getenv('host_db'),
                                port=os.getenv('port_db'),
                                database=os.getenv('database_db'))

        # Open a cursor to perform database operations
        cur = conn.cursor()

        # Execute a query
        for code in codes:
            print(
                f"INSERT INTO flight_search_airportcode (airport_name, country, city, iata_code, icao_code, rus_code, type, webpage) VALUES ('{code['airport_name']}', '{code['country']}', '{code['city']}', '{code['iata_code']}', '{code['icao_code']}', '{code['rus_code']}', '{code['type']}', '{code['webpage']}')")
            cur.execute(
                f"INSERT INTO flight_search_airportcode (airport_name, country, city, iata_code, icao_code, rus_code, type, webpage) VALUES ('{code['airport_name']}', '{code['country']}', '{code['city']}', '{code['iata_code']}', '{code['icao_code']}', '{code['rus_code']}', '{code['type']}', '{code['webpage']}')")

        conn.commit()
        cur.execute("SELECT * FROM flight_search_airportcode")
        # Retrieve query results
        records = cur.fetchall()
        for r in records:
            print(r)

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if conn:
            cur.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто")
