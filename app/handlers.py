from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from truancy import create_doc, test
from app.FSM import Ai
from app.ai import main


router = Router()


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
