import sqlite3 as sq
from datetime import datetime

async def connect_db():
    db = sq.connect("tg.db")
    cur = db.cursor()
    return db, cur

async def close_db(db, cur):
    cur.close()
    db.close()

async def db_start():
    db, cur = await connect_db()
    cur.execute("CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY, times TEXT, latitude REAL, longitude REAL)")
    db.commit()
    cur.close()
    await close_db(db, cur)

async def create_profile(user_id):
    db, cur = await connect_db()
    user = cur.execute("SELECT 1 FROM profile WHERE user_id == ?", (user_id,)).fetchone()
    if not user:
        cur.execute("INSERT INTO profile (user_id, times, latitude, longitude) VALUES (?, NULL, NULL, NULL)", (user_id,))
        db.commit()
    await close_db(db, cur)