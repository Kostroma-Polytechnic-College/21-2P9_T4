from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from keyboards import keyboard

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Добро пожаловать",reply_markup=keyboard.main_kb)
