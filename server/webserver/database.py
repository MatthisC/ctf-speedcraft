import psycopg2
import os


# Variables d'environnement
POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_HOST = os.environ["POSTGRES_HOST"]
POSTGRES_DB = os.environ["POSTGRES_DB"]


def connectToDatabase():
    print("Connecting to database... ", end="")
    conn = psycopg2.connect(user=POSTGRES_USER,
                            password=POSTGRES_PASSWORD,
                            host=POSTGRES_HOST,
                            port="5432",
                            database=POSTGRES_DB)
    print("Established !")
    cur = conn.cursor()
    return conn, cur