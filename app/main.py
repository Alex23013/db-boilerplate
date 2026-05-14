import os
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI(title="FastAPI + Postgres + Mongo")

POSTGRES_URL = os.environ["POSTGRES_URL"]
mongo_client = MongoClient(os.environ["MONGO_URL"])


def get_pg_conn():
    return psycopg2.connect(POSTGRES_URL)


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/health/postgres")
def health_postgres():
    with get_pg_conn() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT version() AS version;")
        return cur.fetchone()


@app.get("/health/mongo")
def health_mongo():
    info = mongo_client.server_info()
    return {"mongo_version": info["version"]}
