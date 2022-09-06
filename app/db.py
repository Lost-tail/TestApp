from functools import wraps
from typing import Type, List
from datetime import date
import psycopg2
from settings import settings
from models import BaseModel, Order



def inject_db_session(function):
    """Pass db session to the wrapped function."""
    
    @wraps(function)
    def wrapped(*args, **kwargs):
        conn = psycopg2.connect(dbname=settings.POSTGRES_DB, user=settings.POSTGRES_USER, 
                        password=settings.POSTGRES_PASSWORD, host=settings.POSTGRES_HOST)
        cursor = conn.cursor()
        try:
            return function(*args, db=cursor, **kwargs)
        finally:
            conn.commit()
            cursor.close()
            conn.close()     
    return wrapped


class Table():

    @inject_db_session
    def __init__(self, name, model: Type[BaseModel], db) -> None:
        self.table_name = f"{settings.PROJECT_NAME}_{name}"
        self.model = model
        sql_query = f"CREATE TABLE IF NOT EXISTS {self.table_name} ({self.model.sql_description()})"
        db.execute(sql_query)

    @inject_db_session
    def get_rows(self, db, **kwargs):
        """Извлекает записи из таблицы бд"""
        var_number = 2
        vars = []
        sql_query = "SELECT * FROM %s "
        if kwargs:
            sql_query += "WHERE "
            for key in kwargs:
                sql_query += key + "=$%d AND " % var_number
                var_number += 1
                vars.append(kwargs[key])
                sql_query = sql_query[:-4]
        db.execute(sql_query, self.table_name, *vars)
        return db.fetchall()


    @inject_db_session
    def update_table(self, data: List[BaseModel], db):
        columns = self.model.columns()
        sql_query = f"INSERT INTO {self.table_name} ({', '.join(columns)}) "
        sql_query += "VALUES "
        sql_query += ('(' + '%s, '*(len(columns)-1 ) + '%s' + '), ')*(len(data)-1)
        sql_query += '(' + '%s, '*(len(columns)-1) + '%s' + ') '
        sql_query += f"ON CONFLICT ({self.model.pk_field}) DO UPDATE SET "
        sql_query += ', '.join((f"{x}=EXCLUDED.{x}" for x in columns))
        query_data = []
        for item in data:
            query_data.extend(item.get_data())
        return db.execute(sql_query, query_data)


data = [
    Order(order_id=1, order_number=1202403, price_usd=60, delivery_time=date.today()),
    Order(order_id=2, order_number=1544403, price_usd=160, delivery_time=date.today())
    ]

orderTable = Table('order', Order)