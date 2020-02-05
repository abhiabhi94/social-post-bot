import json
import MySQLdb
from creds.read_creds import read_cred_file

DB_FILE = 'db_creds.json'


def db_close(cx, conn):
    """
    Commit and close the connection to the database

    Returns
        None

    Params
        cx: MySQLdb cursor object
        conn: mysql connection object
    """
    conn.commit()
    cx.close()
    conn.close()


def db_connect():
    """
    Returns
        A tuple containing
            name of the table inside the database
            name of the column inside the table where links will be stored
            MySQLdb cursor object
            mysql connection object
    Note: Don't forget to close both the objects after use
    """
    db_config = read_cred_file(DB_FILE)
    db_connection = MySQLdb.connect(host=db_config['host'],
                                    user=db_config['user'],
                                    passwd=db_config['password'],
                                    db=db_config['database'],
                                    )
    cursor = db_connection.cursor()

    return db_config['table'], db_config['column'], cursor, db_connection
