import re
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from truancy import create_doc
from app.FSM import Truancy


truancy = Router()


@truancy.callback_query(F.data == 'truancy')
async def doc_one(callback: CallbackQuery, state: FSMContext):

    '''
    Эта функция запрашивает
    номер, дату и время
    составления акта
    '''

    await callback.answer('')
    await callback.message.answer('Номер акта, дата и время составления акта в формате:\n\n12, 14.08.2022, 13:00')
    await state.set_state(Truancy.act_numb_date_time)


@truancy.message(StateFilter(Truancy.act_numb_date_time))
async def doc_one(message: Message, state: FSMContext):

    '''
    Эта функция принимает номер, 
    дату и время составления акта 
    и проверяет их корректность
    '''

    input_data = message.text.strip()

    try:
        number_part, date_part, time_part = input_data.split(',')
    except ValueError:
        await message.answer("Неправильный формат. Используйте 12, 14.08.2022, 13:00")
        return

    date_parts = date_part.strip().split('.')
    if len(date_parts) != 3:
        await message.answer("Неправильный формат даты. Используйте ДД.ММ.ГГГГ.")
        return
    day, month, year = map(int, date_parts)
    if not (1 <= day <= 31) or not (1 <= month <= 12):
        await message.answer("Некорректная дата.")
        return

    time_parts = time_part.strip().split(':')
    if len(time_parts) != 2:
        await message.answer("Неправильный формат времени. Используйте ЧЧ:ММ.")
        return

    await state.update_data(ah=message.text)
    await message.answer('ФИО сотрудника, который не вышел на смену')
    await state.set_state(Truancy.workers)


@truancy.message(StateFilter(Truancy.workers))
async def doc_one(message: Message, state: FSMContext):

    '''
    Эта функция принимает ФИО сотрудника, 
    который не вышел на смену и проверяет 
    их корректность
    '''

    name = message.text.strip()

    if len(name.split()) < 3:
        await message.answer("Пожалуйста, введите полное ФИО сотрудника (фамилия, имя и отчество).")
        return

    if not re.match(r'^[А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+$', name):
        await message.answer("Пожалуйста, убедитесь, что ФИО написано корректно (с заглавной буквы).")
        return

    # Извлечение фамилии, имени и отчества
    last_name, first_name, patronymic = name.split()
    
    # Получение инициалов
    initials = f"{first_name[0]}. {patronymic[0]}."

    # Сохранение данных в состоянии
    await state.update_data(name=name, last_name=last_name, first_name=first_name, patronymic=patronymic, initials=initials)

    await state.update_data(name=message.text)
    await message.answer('Дата и время невыхода сотрудника в формате:\n\n14.08.2022, 13:00')
    await state.set_state(Truancy.truancy_date_time)


@truancy.message(StateFilter(Truancy.truancy_date_time))
async def doc_one(message: Message, state: FSMContext):

    '''
    Эта функция запускает финальную
    функцию "create_doc" для создания
    документа со всеми переменными
    '''

    await state.update_data(time=message.text)
    await create_doc(message=message, state=state)