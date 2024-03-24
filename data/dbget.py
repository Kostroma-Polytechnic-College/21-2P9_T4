from data import database
from datetime import datetime

async def get_user(user_id):
    db, cur = await database.connect_db()
    user = cur.execute("SELECT times FROM profile WHERE user_id == ?", (user_id,)).fetchone()
    await database.close_db(db, cur)
    return user[0] if user else "не указан"

async def get_listUsers(nearest_time):
    db, cur = await database.connect_db()
    cur.execute("SELECT user_id FROM profile WHERE times = ?", (nearest_time,))
    results = cur.fetchall()
    await database.close_db(db, cur)
    return results

async def get_nearestTime():
    db, cur = await database.connect_db()
    current_time = datetime.now().strftime("%H:%M")
    cur.execute("SELECT times FROM profile")
    times = cur.fetchall()
    nearestTime = min(times, key=lambda x: abs(datetime.strptime(x[0], '%H:%M') - datetime.strptime(current_time, '%H:%M')))[0]
    await database.close_db(db, cur)
    return nearestTime

async def get_geo(user_id):
    db, cur = await database.connect_db()
    user = cur.execute("SELECT latitude, longitude FROM profile WHERE user_id == ?", (user_id,)).fetchone()
    await database.close_db(db, cur)
    return user if user else "не указан"