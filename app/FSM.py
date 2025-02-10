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
    truancy_worker = State() # фио сотрудника, который отсутствовал
    truancy_date_time = State() # дата и время смены сотрудника
    check = State() # доп проверка по пропускной системе
    managers = State() # фио подписавших акт