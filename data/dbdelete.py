from data import database

async def delete_time(user_id):
    db, cur = await database.connect_db()
    cur.execute("UPDATE profile SET times = NULL WHERE user_id = ? AND times IS NOT NULL", (user_id,))
    db.commit()
    if cur.rowcount > 0:
        result = True  
    else:
        result = False
    await database.close_db(db, cur)
    return result