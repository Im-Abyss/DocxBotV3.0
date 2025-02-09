import io
from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from docxtpl import DocxTemplate



async def test(message: Message):
    await message.answer('Ты абоба кста')


async def create_doc(message: Message):
    
    # Получаем файл от пользователя
    file_id = message.document.file_id
    file = await message.bot.get_file(file_id)
    file_bytes = await message.bot.download_file(file.file_path)

    # Загружаем документ в память
    doc_stream = io.BytesIO(file_bytes.read())
    doc = DocxTemplate(doc_stream)

    city = 'Ростов-на-Дону'
    c_numb = '2238/2024'
    a_data = '01.11.2024'
    a_time = '19:00'
    f_name = 'Клименко Вероника Сергеевна'
    r_name = 'Стетюха Александр Анатольевич'
    wd = '01.11.2024'
    bh = '09'
    bm = '00'
    eh = '18'
    em = '30'

    '''
    Нужно сделать функционал, при 
    котором переменные выше будет
    задавать пользователь
    '''

    context = {
        'city': city, # город
        'contract': c_numb, # номер договора
        'act_data': a_data, # дата составления акта
        'act_time': a_time, # время составления акта
        'full_name': f_name, # фио сотрудника
        'r_name': r_name, # имя руководителя
        'work_data': wd, # дата невыхода
        'begin_time_hour': bh, # часы начала смены
        'begin_time_minute': bm, # минуты начала смены
        'end_time_hour': eh, # часы окончания смены
        'end_time_minute': em, # минуты окончания смены
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