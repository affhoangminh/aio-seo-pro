import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "profiles.db")


def get_proxies():

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM proxies")
        return cur.fetchall()


def add_proxy(host, port, username="", password=""):

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO proxies (host, port, username, password)
        VALUES (?, ?, ?, ?)
        """, (host, port, username, password))


def update_proxy(proxy_id, host, port, username, password):

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()

        cur.execute("""
        UPDATE proxies
        SET host=?, port=?, username=?, password=?
        WHERE id=?
        """, (host, port, username, password, proxy_id))


def delete_proxy(proxy_id):

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM proxies WHERE id=?",
            (proxy_id,)
        )


def add_proxy_bulk(proxy_list):

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()

        cur.executemany("""
        INSERT INTO proxies (host, port, username, password)
        VALUES (?, ?, ?, ?)
        """, proxy_list)