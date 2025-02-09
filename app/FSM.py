from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class Ai(StatesGroup):

    ai_message = State()


class Truancy(StatesGroup):

    '''
    Нужно ещё дописать состояния для
    лиц, подписавших акт, сложность
    в том, что их может быть каждый
    раз по разному в количестве
    '''

    act_numb_date_time = State() # номер, дата и время составления акта
    workers = State() # сотрудники, подписавшие акт
    truancy_date_time = State() # дата и время невыхода
    truancy_create_doc = State() # создание документа