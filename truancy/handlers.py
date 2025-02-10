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
    await callback.message.answer('Номер акта, дата и время составления акта в формате:\n\n12, 14 февраля 2022, 13:00')
    await state.set_state(Truancy.act_numb_date_time)



@truancy.message(StateFilter(Truancy.act_numb_date_time))
async def doc_one(message: Message, state: FSMContext):
    '''
    Эта функция принимает номер, 
    дату и время составления акта 
    и проверяет их корректность и
    запрашивает ФИО сотрудника,
    который не вышел на смену
    '''
    input_data = message.text.strip()
    try:
        number_part, date_part, time_part = input_data.split(',')
    except ValueError:
        await message.answer("Неправильный формат. Используйте 12, 14 февраля 2022, 13:00")
        return

    # Обработка даты
    date_parts = date_part.strip().split()
    if len(date_parts) != 3:
        await message.answer("Неправильный формат даты. Используйте ДД ММММ ГГГГ (например, 14 февраля 2022).")
        return

    day = int(date_parts[0])
    month_str = date_parts[1].lower()
    year = int(date_parts[2])

    # Словарь для преобразования названия месяца в номер месяца
    months = {
        'января': 1,
        'февраля': 2,
        'марта': 3,
        'апреля': 4,
        'мая': 5,
        'июня': 6,
        'июля': 7,
        'августа': 8,
        'сентября': 9,
        'октября': 10,
        'ноября': 11,
        'декабря': 12
    }

    # Проверка месяца
    month = months.get(month_str)
    if month is None:
        await message.answer("Некорректный месяц.")
        return

    # Проверка даты
    if not (1 <= day <= 31) or not (1 <= month <= 12):
        await message.answer("Некорректная дата.")
        return

    # Обработка времени
    time_parts = time_part.strip().split(':')
    if len(time_parts) != 2:
        await message.answer("Неправильный формат времени. Используйте ЧЧ:ММ.")
        return

    hours, minutes = map(int, time_parts)
    if not (0 <= hours < 24):
        await message.answer("Некорректное время: часы должны быть от 0 до 23.")
        return
    if not (0 <= minutes < 60):
        await message.answer("Некорректное время: минуты должны быть от 0 до 59.")
        return

    # Форматируем минуты, чтобы они всегда были двузначными
    minutes_str = str(minutes).zfill(2)

    await state.update_data(
        act_numb=number_part,
        day=day,
        month=month_str,
        year=year,
        hours=hours,
        minutes=minutes_str  # Используем отформатированные минуты
    )
    await message.answer('ФИО сотрудника, который не вышел на смену')
    await state.set_state(Truancy.truancy_worker)



@truancy.message(StateFilter(Truancy.truancy_worker))
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

    last_name, first_name, patronymic = name.split()

    initials = f"{first_name[0]}. {patronymic[0]}."

    await state.update_data(name=name, last_name=last_name, 
                            first_name=first_name, patronymic=patronymic, 
                            initials=initials)
    await message.answer('Дата и время смены сотрудника в формате:\n\n14 июня 2022, 13:00, 21:00')
    await state.set_state(Truancy.truancy_date_time)



@truancy.message(StateFilter(Truancy.truancy_date_time))
async def doc_one(message: Message, state: FSMContext):
    '''
    Эта функция принимает дату
    и время смены сотрудника
    и запрашивает должности и ФИО
    лиц, подписавших акт
    '''
    truancy_date_time = message.text.strip()
    try:
        truancy_date, truancy_start_time, truancy_end_time = truancy_date_time.split(',')
    except ValueError:
        await message.answer("Неправильный формат. Используйте 14 июня 2022, 13:00, 21:00")
        return

    # Обработка даты
    truancy_date = truancy_date.strip().split()
    if len(truancy_date) != 3:
        await message.answer("Неправильный формат даты. Используйте ДД ММММ ГГГГ (например, 14 июня 2022).")
        return

    truancy_day = int(truancy_date[0])
    month_str = truancy_date[1].lower()
    truancy_year = int(truancy_date[2])

    # Преобразование названия месяца в номер месяца
    months = {
        'января': 1,
        'февраля': 2,
        'марта': 3,
        'апреля': 4,
        'мая': 5,
        'июня': 6,
        'июля': 7,
        'августа': 8,
        'сентября': 9,
        'октября': 10,
        'ноября': 11,
        'декабря': 12
    }

    truancy_month = months.get(month_str)
    if truancy_month is None:
        await message.answer("Некорректный месяц.")
        return

    if not (1 <= truancy_day <= 31) or not (1 <= truancy_month <= 12):
        await message.answer("Некорректная дата.")
        return

    # Обработка времени начала смены
    truancy_start_time = truancy_start_time.strip().split(':')
    if len(truancy_start_time) != 2:
        await message.answer("Неправильный формат времени начала. Используйте ЧЧ:ММ.")
        return

    truancy_start_hours, truancy_start_minutes = map(int, truancy_start_time)
    if not (0 <= truancy_start_hours < 24):
        await message.answer("Некорректное время: часы должны быть от 0 до 23.")
        return
    if not (0 <= truancy_start_minutes < 60):
        await message.answer("Некорректное время: минуты должны быть от 0 до 59.")
        return

    # Обработка времени окончания смены
    truancy_end_time = truancy_end_time.strip().split(':')
    if len(truancy_end_time) != 2:
        await message.answer("Неправильный формат времени окончания. Используйте ЧЧ:ММ.")
        return

    truancy_end_hours, truancy_end_minutes = map(int, truancy_end_time)
    if not (0 <= truancy_end_hours < 24):
        await message.answer("Некорректное время: часы должны быть от 0 до 23.")
        return
    if not (0 <= truancy_end_minutes < 60):
        await message.answer("Некорректное время: минуты должны быть от 0 до 59.")
        return

    await state.update_data(
        truancy_day=truancy_day,
        truancy_month=month_str,
        truancy_year=truancy_year,
        truancy_start_hours=truancy_start_hours,
        truancy_start_minutes=truancy_start_minutes,
        truancy_end_hours=truancy_end_hours,
        truancy_end_minutes=truancy_end_minutes
    )
    
    await message.answer('Дата и время дополнительной проверки по пропускной системе в формате:\n\n14 июня 2022, 17:00')
    await state.set_state(Truancy.check)


@truancy.message(StateFilter(Truancy.check))
async def verification(message: Message, state: FSMContext):

    check_date_time = message.text.strip()
    try:
        check_date, check_time = check_date_time.split(',')
    except ValueError:
        await message.answer("Неправильный формат. Используйте 14 июня 2022, 17:00")
        return

    # Обработка даты
    check_date = check_date.strip().split()
    if len(check_date) != 3:
        await message.answer("Неправильный формат даты. Используйте ДД ММММ ГГГГ (например, 14 июня 2022).")
        return

    check_day = int(check_date[0])
    check_month_str = check_date[1].lower()
    check_year = int(check_date[2])

    # Преобразование названия месяца в номер месяца
    months = {
        'января': 1,
        'февраля': 2,
        'марта': 3,
        'апреля': 4,
        'мая': 5,
        'июня': 6,
        'июля': 7,
        'августа': 8,
        'сентября': 9,
        'октября': 10,
        'ноября': 11,
        'декабря': 12
    }

    check_month = months.get(check_month_str)
    if check_month is None:
        await message.answer("Некорректный месяц.")
        return

    if not (1 <= check_day <= 31) or not (1 <= check_month <= 12):
        await message.answer("Некорректная дата.")
        return

    # Обработка времени начала смены
    check_time = check_time.strip().split(':')
    if len(check_time) != 2:
        await message.answer("Неправильный формат времени начала. Используйте ЧЧ:ММ.")
        return

    check_hours, check_minutes = map(int, check_time)
    if not (0 <= check_hours < 24):
        await message.answer("Некорректное время: часы должны быть от 0 до 23.")
        return
    if not (0 <= check_minutes < 60):
        await message.answer("Некорректное время: минуты должны быть от 0 до 59.")
        return

    await state.update_data(
        check_day=check_day,
        check_month_str=check_month_str,
        check_year=check_year,
        check_hours=check_hours,
        check_minutes=check_minutes
    )

    await message.answer('Должность и ФИО подписавших акт в формате: \n\nдолжность: ФИО, должность: ФИО (и т. д.)')
    await state.set_state(Truancy.managers)



@truancy.message(StateFilter(Truancy.managers))
async def doc_one(message: Message, state: FSMContext):
    '''
    Эта функция принимает должности
    и ФИО подписавших акт, а также
    запускает финальную функцию 
    "create_doc" для создания
    документа со всеми переменными
    '''
    managers_input = message.text.strip()
    
    # Разделяем на подписи по запятой
    signatures = managers_input.split(',')
    
    # Обрабатываем каждую подпись
    processed_signatures = []
    for signature in signatures:
        # Убираем лишние пробелы
        signature = signature.strip()
        if ':' in signature:  # Проверяем, что в подписи есть двоеточие
            position, name = signature.split(':', 1)  # Разделяем на должность и ФИО
            position = position.strip()  # Убираем пробелы
            name = name.strip()  # Убираем пробелы
            
            # Разделяем ФИО на части и берем только фамилию и инициалы
            name_parts = name.split()
            if len(name_parts) >= 2:  # Убедимся, что есть фамилия и хотя бы одно имя
                surname = name_parts[0]  # Фамилия
                initials = ''.join(part[0] + '.' for part in name_parts[1:])  # Инициалы
                processed_signatures.append({'position': position, 'surname': surname, 'initials': initials})  # Сохраняем в виде словаря

    # Сохраняем обработанные подписи в состоянии
    await state.update_data(signatures=processed_signatures)
    await create_doc(message=message, state=state)