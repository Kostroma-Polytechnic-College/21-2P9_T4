from datetime import datetime
from data import database

async def edit_time(state, user_id):
    db, cur = await database.connect_db()
    data = await state.get_data()
    time = data.get('time', '')  
    time = datetime.strptime(time, '%H:%M')
    time = time.strftime("%H:%M")
    cur.execute("UPDATE profile SET times = ? WHERE user_id == ?", (time, user_id))
    db.commit()
    await database.close_db(db, cur)

async def edit_geo(user_id, latitude, longitude):
    db, cur = await database.connect_db()
    cur.execute("UPDATE profile SET latitude = ?, longitude = ?  WHERE user_id == ?", (latitude, longitude, user_id))
    db.commit()
    await database.close_db(db, cur)