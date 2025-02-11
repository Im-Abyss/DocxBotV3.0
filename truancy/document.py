import io
import os

from aiogram import types, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from docxtpl import DocxTemplate



async def test(message: Message):
    await message.answer('Ты абоба кста')



async def create_doc(message: Message, state: FSMContext):
    data = await state.get_data()

    # Извлекаем переменные
    act = data.get('act_numb')
    ad = data.get('day')
    am = data.get('month')
    ay = data.get('year')
    ah = data.get('hours')
    ma = data.get('minutes')
    ln = data.get('last_name')
    fn = data.get('first_name')
    pt = data.get('patronymic')
    inl = data.get('initials')
    wd = data.get('truancy_day')
    wm = data.get('truancy_month')
    wy = data.get('truancy_year')
    bh = data.get('truancy_start_hours')
    bm = data.get('truancy_start_minutes')
    eh = data.get('truancy_end_hours')
    em = data.get('truancy_end_minutes')
    vd = data.get('check_day')
    vm = data.get('check_month_str')
    vy = data.get('check_year')
    vh = data.get('check_hours')
    mv = data.get('check_minutes')

    # Извлекаем подписи
    signatures = data.get('signatures', [])

    # Формируем строку с подписями, разделёнными запятыми
    signatures_str = ', '.join(
        f"{signature['position']} {signature['surname']} {signature['initials']}"
        for signature in signatures
    )

    # Формируем строку с подписями, разделёнными пустыми строками
    signatures_formatted = '\n\n'.join(
        f"{signature['position']} {signature['surname']} {signature['initials']}"
        for signature in signatures
    )

    # Путь к шаблону
    template_path = os.path.join(os.path.dirname(__file__), 'pattern.docx')

    # Загружаем шаблон
    with open(template_path, 'rb') as file:
        doc_stream = io.BytesIO(file.read())

    doc = DocxTemplate(doc_stream)

    # Формируем контекст
    context = {
        'act': act,  # номер акта
        'ad': ad,    # день составления акта
        'am': am,    # месяц составления акта
        'ay': ay,    # год составления акта
        'ah': ah,    # время составления акта
        'ma': ma,    # время составления акта

        'ln': ln,    # имя сотрудника
        'fn': fn,    # фамилия сотрудника
        'pt': pt,    # отчество сотрудника
        'inl': inl,  # инициалы сотрудника

        'wd': wd,    # день невыхода
        'wm': wm,    # месяц невыхода
        'wy': wy,    # год невыхода
        'bh': bh,    # часы начала смены
        'bm': bm,    # минуты начала смены
        'eh': eh,    # часы окончания смены
        'em': em,    # минуты окончания смены
        
        'vd': vd,    # день проверки
        'vm': vm,    # месяц проверки
        'vy': vy,    # год проверки
        'vh': vh,    # часы проверки
        'mv': mv,    # минуты проверки

        'signatures': signatures_str,  # Строка с подписями через запятую
        's_formatted': signatures_formatted  # Строка с подписями через пустые строки
    }

    # Заполняем шаблон
    doc.render(context)

    # Сохраняем изменённый документ
    output_stream = io.BytesIO()
    doc.save(output_stream)
    output_stream.seek(0)

    # Отправляем документ пользователю
    await message.reply_document(
        document=types.BufferedInputFile(file=output_stream.read(), filename='Изменённый.docx')
    )

    # Очищаем состояние
    await state.clear()