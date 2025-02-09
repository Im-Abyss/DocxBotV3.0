from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from truancy import create_doc
from app import Truancy


truancy = Router()


@truancy.callback_query(F.data == 'truancy')
async def doc_one(callback: CallbackQuery, state: FSMContext):

    await callback.answer('Невыходы сотрудников')
    await callback.message.answer('Номер акта')
    await state.set_state(Truancy.act_numb)


@truancy.callback_query(StateFilter(Truancy.act_numb))
async def doc_one(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Дата составления акта')
    await state.set_state(Truancy.act_date)


@truancy.callback_query(StateFilter(Truancy.act_date))
async def doc_one(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Время составления акта')
    await state.set_state(Truancy.act_time)


@truancy.callback_query(StateFilter(Truancy.act_time))
async def doc_one(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('ФИО сотрудника, который не вышел на смену')
    await state.set_state(Truancy.workers)


@truancy.callback_query(StateFilter(Truancy.workers))
async def doc_one(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Дата невыхода сотрудника')
    await state.set_state(Truancy.truancy_date)


@truancy.callback_query(StateFilter(Truancy.truancy_date))
async def doc_one(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Время')
    await state.set_state(Truancy.truancy_time)


@truancy.callback_query(StateFilter(Truancy.truancy_time))
async def doc_one(callback: CallbackQuery, state: FSMContext):
    await create_doc()