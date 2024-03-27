from aiogram.filters import BaseFilter
from aiogram.types import Message
from data import dbget

class CheckDBField(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        result = await dbget.get_geo(message.from_user.id)
        if result is not None and result != (None, None):
            return True
        await message.answer("Прежде чем выполнять это действие, укажите свою геопозицию")
        return False