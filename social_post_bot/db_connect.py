import os
from typing import NamedTuple

import pymysql.cursors


class Database(NamedTuple):
    table: str
    column: str
    connection: pymysql.connections.Connection


def connect() -> Database:
    connection = pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        cursorclass=pymysql.cursors.DictCursor
    )

    return Database(
        table=os.getenv('DB_TABLE', 'my_links'),
        column=os.getenv('DB_COLUMN', 'link'),
        connection=connection
    )
