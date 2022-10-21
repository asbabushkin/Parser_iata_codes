"""
* fill_airportcodes - заполнение таблицы 'flight_search_airportcode' в БД;
* fill_citycodes - заполнение таблицы 'flight_search_citycode' в БД.
"""

import psycopg2
import os
from psycopg2 import Error
from dotenv import load_dotenv

load_dotenv()


def fill_airportcodes(codes):
    try:
        conn = psycopg2.connect(user=os.getenv('user_db'),
                                password=os.getenv('password_db'),
                                host=os.getenv('host_db'),
                                port=os.getenv('port_db'),
                                database=os.getenv('database_db'))

        cur = conn.cursor()
        for code in codes:
            cur.execute(
                f"INSERT INTO flight_search_airportcode (airport_name, country, city, iata_code, icao_code, rus_code, type, webpage) VALUES ('{code['airport_name']}', '{code['country']}', '{code['city']}', '{code['iata_code']}', '{code['icao_code']}', '{code['rus_code']}', '{code['type']}', '{code['webpage']}')")
        conn.commit()

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if conn:
            cur.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто")
        else:
            print('Не удалось установить соединение с БД')


def fill_citycodes(codes):
    try:
        conn = psycopg2.connect(user=os.getenv('user_db'),
                                password=os.getenv('password_db'),
                                host=os.getenv('host_db'),
                                port=os.getenv('port_db'),
                                database=os.getenv('database_db'))

        cur = conn.cursor()
        for code in codes:
            cur.execute(
                f"INSERT INTO flight_search_citycode (city_eng, city_rus, code_eng, code_rus) VALUES ('{code['city_eng']}', '{code['city_rus']}', '{code['code_eng']}', '{code['code_rus']}')")
        conn.commit()

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if conn:
            cur.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто")
        else:
            print('Не удалось установить соединение с БД')
