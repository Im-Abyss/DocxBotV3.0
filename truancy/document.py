import io
import os

from aiogram import types, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from docxtpl import DocxTemplate



async def test(message: Message):
    await message.answer('Ты абоба кста')


import io
from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from docxtpl import DocxTemplate
import os

router = Router()

async def create_doc(message: Message, state: FSMContext):

    template_path = os.path.join(os.path.dirname(__file__), 'pattern.docx')

    with open(template_path, 'rb') as file:
        doc_stream = io.BytesIO(file.read())

    doc = DocxTemplate(doc_stream)

    act = '24'
    ad = '09'
    am = 'месяц'
    ay = '2022'
    ah = '19'
    am = '00'
    name = 'Клименко Вероника Сергеевна'
    book = 'Черкасов Александр Алексеевич'
    hr = 'Белова Анна Анатольевна'
    secr = 'Калугин Артём Александрович'
    wd = '01.11.2024'
    bh = '09'
    bm = '00'
    eh = '18'
    em = '30'

    context = {
        'act': act,  # номер акта
        'ad': ad,  # день составления акта
        'ad': am,  # месяц составления акта
        'ad': ay,  # год составления акта
        'ah': ah,  # время составления акта
        'am': am,  # время составления акта
        'name': name,  # фио сотрудника
        'book': book,  # фио гл бухгалтера
        'hr': hr,  # фио специалиста по кадрам
        'secr': secr,  # фио секретаря
        'wd': wd,  # дата невыхода
        'bh': bh,  # часы начала смены
        'bm': bm,  # минуты начала смены
        'eh': eh,  # часы окончания смены
        'em': em,  # минуты окончания смены
    }

    doc.render(context)

    output_stream = io.BytesIO()
    doc.save(output_stream)
    output_stream.seek(0)

    await message.reply_document(
        document=types.BufferedInputFile(file=output_stream.read(), filename='Изменённый.docx')
    )

    await state.clear