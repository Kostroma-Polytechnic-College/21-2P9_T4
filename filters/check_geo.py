from aiogram.filters import BaseFilter
from aiogram.types import Message
from data import database

class CheckDBField(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        db, cur = await database.connect_db()
        result = cur.execute("SELECT latitude FROM profile WHERE user_id = ?", (message.from_user.id,)).fetchone()
        await database.close_db(db, cur)
        if result:
            return True
        await message.answer("Прежде чем выполнять это действие, укажите свою геопозицию")
        return False