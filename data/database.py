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
    cur.execute("CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY, times TEXT)")
    db.commit()
    cur.close()
    await close_db(db, cur)

async def create_profile(user_id, time):
    db, cur = await connect_db()
    user = cur.execute("SELECT 1 FROM profile WHERE user_id == ?", (user_id,)).fetchone()
    if not user:
        cur.execute("INSERT INTO profile VALUES(?, ?)", (user_id, time))
        db.commit()
    await close_db(db, cur)

async def edit_profile(state, user_id):
    db, cur = await connect_db()
    data = await state.get_data()
    time = data.get('time', '')  
    time = datetime.strptime(time, '%H:%M')
    time = time.strftime("%H:%M")
    cur.execute("UPDATE profile SET times = ? WHERE user_id == ?", (time, user_id))
    db.commit()
    await close_db(db, cur)

async def get_user(user_id):
    db, cur = await connect_db()
    user = cur.execute("SELECT times FROM profile WHERE user_id == ?", (user_id,)).fetchone()
    await close_db(db, cur)
    return user[0] if user else "не указан"

async def get_listUsers(nearest_time):
    db, cur = await connect_db()
    cur.execute("SELECT user_id FROM profile WHERE times = ?", (nearest_time,))
    results = cur.fetchall()
    await close_db(db, cur)
    return results

async def get_nearestTime():
    db, cur = await connect_db()
    current_time = datetime.now().strftime("%H:%M")
    cur.execute("SELECT times FROM profile")
    times = cur.fetchall()
    nearestTime = min(times, key=lambda x: abs(datetime.strptime(x[0], '%H:%M') - datetime.strptime(current_time, '%H:%M')))[0]
    await close_db(db, cur)
    return nearestTime

async def delete_user(user_id):
    db, cur = await connect_db()
    cur.execute("DELETE FROM profile WHERE user_id = ?", (user_id,))
    db.commit()
    if cur.rowcount > 0:
        result = True  
    else:
        result = False
    await close_db(db, cur)
    return result