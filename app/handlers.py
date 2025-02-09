from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from truancy import create_doc, test
from .FSM import Ai
from .ai import main


router = Router()


@router.message(F.text == 'Я абоба')
async def test_document(message: Message):
    await test(message=message)


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