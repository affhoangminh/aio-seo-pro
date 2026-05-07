import sqlite3
import json

DB_PATH = "database/profiles.db"


# ==========================
# INIT DATABASE
# ==========================

def init_db():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # profiles table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        proxy_id INTEGER,
        fingerprint TEXT
    )
    """)

    # proxies table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS proxies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        host TEXT,
        port TEXT,
        username TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


# ==========================
# ADD PROFILE
# ==========================

def add_profile(name, proxy_id=None, fingerprint=None):

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    if fingerprint is None:
        fingerprint = {}

    cur.execute("""
    INSERT INTO profiles (name, proxy_id, fingerprint)
    VALUES (?, ?, ?)
    """, (name, proxy_id, json.dumps(fingerprint)))

    conn.commit()
    conn.close()


# ==========================
# GET PROFILES
# ==========================

def get_profiles():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    SELECT
        profiles.id,
        profiles.name,
        proxies.host,
        proxies.port,
        proxies.username,
        proxies.password
    FROM profiles
    LEFT JOIN proxies
    ON profiles.proxy_id = proxies.id
    """)

    rows = cur.fetchall()

    conn.close()

    return rows


# ==========================
# UPDATE PROFILE
# ==========================

def update_profile(profile_id, name, proxy_id):

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    UPDATE profiles
    SET name=?, proxy_id=?
    WHERE id=?
    """, (name, proxy_id, profile_id))

    conn.commit()
    conn.close()


# ==========================
# DELETE PROFILE
# ==========================

def delete_profile(profile_id):

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM profiles WHERE id=?",
        (profile_id,)
    )

    conn.commit()
    conn.close()


# ==========================
# GET SINGLE PROFILE
# ==========================

def get_profile(profile_id):

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    SELECT
        profiles.id,
        profiles.name,
        proxies.host,
        proxies.port,
        proxies.username,
        proxies.password
    FROM profiles
    LEFT JOIN proxies
    ON profiles.proxy_id = proxies.id
    WHERE profiles.id=?
    """, (profile_id,))

    row = cur.fetchone()

    conn.close()

    return row