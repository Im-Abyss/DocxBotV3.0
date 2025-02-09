import asyncio
from aiogram import Bot, Dispatcher

from config import TOKEN
from app import router


bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(router)    
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass