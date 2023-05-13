import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# уровни логa 
logging.basicConfig(level=logging.INFO)

# инициализация
bot = Bot(token="6186633362:AAFhZSgNuoUGPsQDLpZimy62_luIibwD060")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# настройка клавиатуры
keyboard = InlineKeyboardMarkup(row_width=1)
#keyboard.add(InlineKeyboardButton("Назад", callback_data='back_to_menu'))        

# ссылки и текст
about_college_text = "АЛМАТИНСКИЙ ГОСУДАРСТВЕННЫЙ ПОЛИТЕХНИЧЕСКИЙ КОЛЛЕДЖ\nКолледж находится в рейтинге «ТОП-10» лучших колледжей Республики Казахстан. В мае 2017 года колледж первым в регионе прошел Международную институциональную и специализированную аккредитацию и работает в соответствии с требованиями международной Системы менеджмента и качества. В колледже создана современная инфраструктура, функционирует Goworking-centre, Центр обслуживания студентов, StartUp площадка для продвижения бизнес-идей, Wi-Fi, столовая на 150 посадочных мест, спортивный зал, открытая спортивная площадка, актовый зал на 100 посадочных мест, имеется более 100 000 единиц библиотечного фонда, 1 копировальный центр, доступ к электронной библиотеке ведущих научных и исследовательских журналов и книг, 13 компьютерных классов, 50 единиц проекционного оборудования, 350 компьютеров, современные лаборатории электроники «Delta Chip», «Кибербезопасность», «3D-принтинг», «Web программирования», «Робототехники». После окончания колледжа у выпускников есть возможность продолжить обучение в ВУЗе по сокращенной программе. г. Алматы Основан в 1940 г."
college_social_links = "Ссылки на соц. сети колледжа: \nInstagram - https://instagram.com/polytechalmaty?igshid=YmMyMTA2M2Y= \nTikTok - https://www.tiktok.com/@polytech_college?_t=8WNbG2CEXva&_r=1 \nОфициальный сайт - https://almatypolytech.edu.kz/ \nYouTube - https://www.youtube.com/channel/UC0mlIq6b97sX5vfWLpEWdPA/videos"
prof_test_link = "Можете пройти тест по проф ориентации: \n https://edunavigator.kz/ru"
list_of_documents = "При подаче в канцелярию колледжа: \n 1) заявление о приеме документов; \n 2) подлинник документа об образовании (Аттестат); \n 3) фотографии размером 3х4 см в количестве 4-х штук; \n4) медицинская справка формы № 075-У, для инвалидов I и II группы и инвалидов с детства заключение медико-социальной экспертизы по форме 031-У;\n5) документ, удостоверяющий личность (для идентификации личности).\n\n\nПри подаче через веб-портал «Электронного правительства»: www. egov.kz: \n 1) заявление одного из родителей (или иных законных представителей) услугополучателя в форме электронного документа, подписанного ЭЦП его представителя, с указанием фактического места жительства услугополучателя: \n2) электронная копия документа об образовании или документ об образовании в электронном виде: \n 3) электронные копии документов медицинских справок по форме № 075-У, для инвалидов I и II грушпы и инвалидов с детства заключение медико-социальной экспертизы по форме 031-У;\n 4) цифровая фотография размером 3х4 см.\n 5) Сведения о документе, удостоверяющего личность услугополучателя, услугодатель получает из соответствующих государственных информационных систем через шоз «электронного правительства»"
contact_info = "Адрес: Казахстан, Алматы, микрорайон Тастак-1, 1В \n\n Телефон: +7 727 393 39 52\n Моб.номер: +7 702 958 26 37\n Почта: info@agpk.kz"

# список профессий(квалификации)
PROFESSIONS = [
    {"name": "Техник сетевого и системного админстрирования", "url": "https://almatypolytech.edu.kz/page/87"},
    {"name": "Оператор компьютерного и аппаратного обеспечения", "url": "https://almatypolytech.edu.kz/page/87"},
    {"name": "Разработчик программного обеспечения", "url": "https://almatypolytech.edu.kz/page/88"},
    {"name": "Техник информационных систем", "url": "https://almatypolytech.edu.kz/page/88"},
    {"name": "Техник информационной безопасности", "url": "https://almatypolytech.edu.kz/page/89"},
    {"name": "Техник мультимедийных и цифровых систем", "url": "https://almatypolytech.edu.kz/page/90"},
    {"name": "Электромонтажник-наладчик телекоммуникационного оборудования и каналов связи", "url": "https://almatypolytech.edu.kz/page/90"},
    {"name": "Техник-механик", "url": "https://almatypolytech.edu.kz/page/91"},
]

# результаты
RESULTS = [
    {"name": "Списки зачисленных", "url": "https://drive.google.com/file/d/1wYkHznqqkPt-l2e56yhTNMp_bvvMXNay/edit?rtpof=true&sd=true"},
    {"name": "Приказ о зачислении", "url": "https://almatypolytech.edu.kz/page/108"}
]

# состояние FSM p.s: получение клавиатуры меню
class AboutCollege(StatesGroup):
    menu = State()
class ChooseProfeccion(StatesGroup):
    menu = State()  
class Enrollment(StatesGroup):
    menu = State()  
class FeedBack(StatesGroup):
    menu = State() 

# получение меню
def get_menu_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("О колледже", callback_data='about_college'),
        InlineKeyboardButton("Выбор профессии", callback_data='choose_profession'),
        InlineKeyboardButton("Наши специальности", callback_data='professions'),
        InlineKeyboardButton("Поступление", callback_data='enrollment'),
        InlineKeyboardButton("Результаты", callback_data='results'),
        InlineKeyboardButton("Контакты", callback_data='contacts')
    )
    return keyboard

# /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    # отправляем приветственное сообщение и главное меню
    await message.answer("Привет! Я бот для абитуриентов АГПК. Чем я могу вам помочь?", reply_markup=get_menu_keyboard())

# "О колледже"
@dp.callback_query_handler(text='about_college')
async def about_college(callback_query: types.CallbackQuery):
    await callback_query.message.answer(about_college_text)
    await callback_query.message.answer(college_social_links)
    await callback_query.message.answer(reply_markup=keyboard)

# "Выбор профессии"
@dp.callback_query_handler(text='choose_profession')
async def choose_profession(callback_query: types.CallbackQuery):
    #await ChooseProfeccion.menu.set()
    await callback_query.message.answer(f"{prof_test_link}", reply_markup=keyboard)

profession_callback = CallbackData("profession", "index")

professions_keyboard = InlineKeyboardMarkup(row_width=2)

profession_handlers = {}

for index, profession in enumerate(PROFESSIONS):
    button = InlineKeyboardButton(profession["name"], url=profession["url"])
    professions_keyboard.add(button)

# добавляем обработчики callback-запросов в Dispatcher(отвечает за обработку входящих сообщений)
for handler in profession_handlers.values():
    dp.register_callback_query_handler(handler)

# "Наши специальности"
@dp.callback_query_handler(text='professions')
async def show_professions(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Выберите квалификацию:", reply_markup=professions_keyboard)

# "Поступление"
@dp.callback_query_handler(text='enrollment')
async def enrollment(callback_query: types.CallbackQuery):
    await callback_query.message.answer(list_of_documents)
    await callback_query.message.answer(reply_markup=keyboard)

result_callback = CallbackData("result", "index")

results_keyboard = InlineKeyboardMarkup(row_width=2)

result_handlers = {}

for index, result in enumerate(RESULTS):
    button = InlineKeyboardButton(result["name"], url=result["url"])
    results_keyboard.add(button)


for handler in result_handlers.values():
    dp.register_callback_query_handler(handler)

# "Результаты"
@dp.callback_query_handler(text='results')
async def show_results(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Результаты 2022-2023 учебного года:", reply_markup=results_keyboard)

# "Контакты"
@dp.callback_query_handler(text='contacts')
async def contacts(callback_query: types.CallbackQuery):
    await callback_query.message.answer(contact_info)
    await callback_query.message.answer(reply_markup=keyboard)
       

# "Назад"
#@dp.callback_query_handler(text='back_to_menu')
#async def back_to_menu(callback_query: types.CallbackQuery):
    #await callback_query.answer()
    #await callback_query.message.edit_reply_markup(reply_markup=get_menu_keyboard())


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp)

