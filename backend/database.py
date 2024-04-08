from flask import Flask
from dbutils.pooled_db import PooledDB
import mysql.connector

pool = None

def create_pool(app):
    global pool
    try:
        db_config = app.config['DATABASE']
        pool = PooledDB(
            creator=mysql.connector,
            mincached=1,
            maxcached=10,
            **db_config
        )
    except Exception as e:
        print("Error occurred while creating database pool:", e)

def get_db():
    return pool.connection()

def close_db(e=None):
    if pool:
        pool.close()

def init_app(app):
    create_pool(app)
    app.teardown_appcontext(close_db)

app = Flask(__name__)

if __name__ == "__main__":
    init_app(app)
    app.run(debug=True)
