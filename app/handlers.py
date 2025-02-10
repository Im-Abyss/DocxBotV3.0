from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from truancy import create_doc, test
from app.FSM import Ai
from app.ai import main


router = Router()


@router.message(F.text == 'Я абоба')
async def test_document(message: Message):
    await test(message=message)


@router.message(CommandStart())
async def start(message: Message):
    await message.answer('Здравствуйте, пожалуйста, выберите документ.', 
                         reply_markup=kb.keyboard_truancy)


@router.message(F.document)
async def handle_document(message: Message):
    await create_doc(message=message)


@router.message(Command('ai'))
async def ai_help(message: Message, state: FSMContext):
    await message.answer('Напишите пожалуйста ваш запрос 😊')
    await state.set_state(Ai.ai_message)


@router.message(StateFilter(Ai.ai_message))
async def try_ai(message: Message, state: FSMContext):
    content = message.text
    response = await main(content=content)
    await message.answer(response)
    state.clear

# @router.message(Command('test'))
# async def send_docx_file(message: Message):
#     # Путь к файлу в папке проекта
#     file_path = os.path.join(os.path.dirname(__file__), 'pattern.docx')

#     # Открываем файл в бинарном режиме
#     with open(file_path, 'rb') as file:
#         file_bytes = file.read()

#     # Создаем BytesIO объект для отправки
#     file_stream = io.BytesIO(file_bytes)
#     file_stream.seek(0)

#     # Отправляем файл пользователю
#     await message.reply_document(
#         document=types.BufferedInputFile(file=file_stream.read(), filename='pattern.docx')
#     )