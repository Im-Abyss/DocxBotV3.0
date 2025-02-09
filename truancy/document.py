import io
from aiogram import types, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from docxtpl import DocxTemplate



async def test(message: Message):
    await message.answer('Ты абоба кста')


async def create_doc(message: Message, state: FSMContext):
    
    # Получаем файл от пользователя
    file_id = message.document.file_id
    file = await message.bot.get_file(file_id)
    file_bytes = await message.bot.download_file(file.file_path)

    # Загружаем документ в память
    doc_stream = io.BytesIO(file_bytes.read())
    doc = DocxTemplate(doc_stream)

    act = '24'
    ad = '09.05.2022'
    ah = '19:00'
    name = 'Клименко Вероника Сергеевна'
    book = 'Стетюха Александр Анатольевич'
    hr = ''
    secr = ''
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
        'act': act, # номер акта
        'ad': ad, # дата составления акта
        'ah': ah, # время составления акта
        'name': name, # фио сотрудника
        'book': book, # фио гл бухгалтера
        'hr': hr, # фио специалиста по кадрам
        'secr': secr, # фио секретаря
        'wd': wd, # дата невыхода
        'bh': bh, # часы начала смены
        'bm': bm, # минуты начала смены
        'eh': eh, # часы окончания смены
        'em': em, # минуты окончания смены
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