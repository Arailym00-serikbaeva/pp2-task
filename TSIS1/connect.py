import psycopg2
from config import db_params

def get_connection():
    try:
        conn = psycopg2.connect(**db_params)
        return conn
    except Exception as e:
        print(f"Қосылу қатесі: {e}")
        return None