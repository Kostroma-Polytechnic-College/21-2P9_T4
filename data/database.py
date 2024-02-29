import sqlite3 as sq
from datetime import datetime

db = sq.connect("tg.db")
cur = db.cursor()

async def db_start():
    global db, cur
    cur.execute("CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY, times TEXT)")
    db.commit()

async def create_profile(user_id, time):
    user = cur.execute("SELECT 1 FROM profile WHERE user_id == ?", (user_id,)).fetchone()
    if not user:
        cur.execute("INSERT INTO profile VALUES(?, ?)", (user_id, time))
        db.commit()

async def edit_profile(state, user_id):
    data = await state.get_data()
    time = data.get('time', '')  
    time = datetime.strptime(time, '%H:%M')
    time = time.strftime("%H:%M")
    cur.execute("UPDATE profile SET times = ? WHERE user_id == ?", (time, user_id))
    db.commit()

async def get_user(user_id):
    user = cur.execute("SELECT times FROM profile WHERE user_id == ?", (user_id,)).fetchone()
    return user[0] if user else "не указан"