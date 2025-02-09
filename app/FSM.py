from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class Ai(StatesGroup):

    ai_message = State()


class Truancy(StatesGroup):

    act_numb = State() # номер акта
    act_date = State() # дата составления акта
    act_time = State() # время составления акта
    workers = State() # сотрудники, подписавшие акт
    truancy_date = State() # дата невыхода
    truancy_time = State() # время невыхода
    truancy_create_doc = State()