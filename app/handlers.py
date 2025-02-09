import io
from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from docxtpl import DocxTemplate
from docx import Document

from .ai import main, check_error

router = Router()


class Ai(StatesGroup):

    ai_message = State()


@router.message(F.document)
async def handle_document(message: Message):

    # Получаем файл от пользователя
    file_id = message.document.file_id
    file = await message.bot.get_file(file_id)
    file_bytes = await message.bot.download_file(file.file_path)

    # Загружаем документ в память
    doc_stream = io.BytesIO(file_bytes.read())
    doc = DocxTemplate(doc_stream)

    heading = "Это мой документ"
    paragraph = "И этот документ сделал телеграм бот"

    # Данные для вставки в шаблон
    context = {
        "heading": heading,
        "paragraph": paragraph,
    }

    # Заменяем шаблонные переменные в документе
    doc.render(context)

    # Сохраняем изменённый документ в память
    output_stream = io.BytesIO()
    doc.save(output_stream)
    output_stream.seek(0)

    # Отправляем изменённый документ пользователю
    await message.reply_document(
        document=types.BufferedInputFile(file=output_stream.read(), filename='Изменённый.docx')
    )


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