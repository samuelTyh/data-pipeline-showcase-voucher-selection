from typing import Dict, List
import psycopg2
from psycopg2.extras import execute_values


class DB:
    """
    Initialize DB instance
    """
    voucher_selection_schema = {
        "timestamp": "DATE",
        "country_code": "VARCHAR",
        "last_order_ts": "DATE",
        "first_order_ts": "DATE",
        "total_orders": "INT",
        "voucher_amount": "INT",
    }
    voucher_segment_schema = {
        "segment_name": "VARCHAR",
        "voucher_amount": "INT",
    }

    def __init__(self, local=False):
        self.host = '0.0.0.0' if local else "postgres.host"
        self.connection_params = {
            "host": self.host, "database": "voucher_selection", "user": "user", "password": "password", "port": 5432}
        self._connection = None
        self._create_connection()

    def _create_connection(self):
        try:
            print('Connecting to the Postgres...')
            conn = psycopg2.connect(**self.connection_params)
        except Exception as e:
            raise e
        self._connection = conn
        print(f'Database {self.connection_params["database"]} connected successfully')

    def create_main_table(self):
        columns = ", ".join(f"{k} {v}" for k, v in self.voucher_selection_schema.items())
        query = (
            f"""
            CREATE TABLE IF NOT EXISTS voucher_selection (
            id serial PRIMARY KEY, {columns}
            );
            """
        )
        with self._connection.cursor() as cursor:
            cursor.execute(query)
            self._connection.commit()

    def create_segment_table(self):
        columns = ", ".join(f"{k} {v}" for k, v in self.voucher_segment_schema.items())
        query = f"""CREATE TABLE IF NOT EXISTS segments ({columns}, UNIQUE (segment_name));"""
        with self._connection.cursor() as cursor:
            cursor.execute(query)
            self._connection.commit()

    def insert_into_main_table(self, data: List[Dict]):
        if not self._connection:
            self._create_connection()
        values = self.insertion_helper(data)
        columns = ", ".join(f"{k}" for k, _ in self.voucher_selection_schema.items())
        insert_query = (
            f"""
            INSERT INTO voucher_selection ({columns}) VALUES %s
            ON CONFLICT (id) DO NOTHING;
            """
        )
        with self._connection.cursor() as cursor:
            try:
                execute_values(cursor, insert_query, values)
            except Exception as e:
                raise e
        self._connection.commit()

    def insert_into_segment_table(self, data: List[Dict]):
        if not self._connection:
            self._create_connection()
        values = self.insertion_helper(data)
        insert_query = (
            f"""
            INSERT INTO segments (segment_name, voucher_amount) VALUES %s
            ON CONFLICT (segment_name) DO UPDATE SET voucher_amount = EXCLUDED.voucher_amount;
            """
        )
        with self._connection.cursor() as cursor:
            try:
                execute_values(cursor, insert_query, values)
            except Exception as e:
                raise e
        self._connection.commit()

    def get_voucher_amount_from_segment(self, segment_value):
        if segment_value == 'undefined' or not segment_value:
            raise TypeError('No segment found')
        if not self._connection:
            self._create_connection()
        query = f"""SELECT * FROM segments WHERE segment_name = '{segment_value}';"""
        with self._connection.cursor() as cursor:
            cursor.execute(query)
            _, voucher_amount = cursor.fetchone()
        return voucher_amount

    @staticmethod
    def insertion_helper(data: List[Dict]):
        values_set = []
        for obj in data:
            values = [v for _, v in obj.items()]
            values_set.append(tuple(values))
        return values_set
