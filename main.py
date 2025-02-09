import asyncio
from aiogram import Bot, Dispatcher

from config import TOKEN
from app import router
from truancy import truancy


bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    dp.include_router(truancy)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass