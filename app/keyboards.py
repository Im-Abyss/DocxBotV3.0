from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


keyboard_truancy = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Невыходы',
                              callback_data='truancy')
    ]])