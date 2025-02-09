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
    contract = '2238/2024'
    act_data = '01.11.2024'
    act_time = '19:00'
    full_name = 'Клименко Вероника Сергеевна'
    work_data = '01.11.2024'
    begin_time_hour = '09'
    begin_time_minute = '00'
    end_time_hour = '18'
    end_time_minute = '30'

    '''
    Нужно сделать функционал, при 
    котором переменные выше будет
    задавать пользователь
    '''

    context = {
        'city': city,
        'contract': contract,
        'act_data': act_data, 
        'act_time': act_time,
        'full_name': full_name,
        'work_data': work_data,
        'begin_time_hour': begin_time_hour, 
        'begin_time_minute': begin_time_minute, 
        'end_time_hour': end_time_hour, 
        'end_time_minute': end_time_minute,
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