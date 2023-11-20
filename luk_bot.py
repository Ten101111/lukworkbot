from io import BytesIO

from aiogram.types import Message

from configuration import admin_id
from main import bot, dp


from aiogram.dispatcher.filters.state import State, StatesGroup
import calendar, locale
from  PIL import Image, ImageDraw, ImageFont
from aiogram import types


async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id, text="Бот запущен!")

class PreviousCommandState(StatesGroup):
    previous_command = State()

@dp.message_handler(commands=['start'])
async def strter(message: Message):
    text = f'👋Привет, <b>{message.from_user.first_name}</b>!\n' \
    f'\n' \
    f'🤝🏻Тебя приветствует телеграмм бот <b>ООО "Лукойл Центрнефтепродукт"</b>!\n' \
    f'\n' \
    f'🫵🏻Здесь ты можешь получить информацию о своей смене в этом месяце.\n' \
    f'\n' \
    f'⛽️Введите номер Вашей АЗС в формате: <u><b>77551</b></u>\n' \
    f'\n' \
    f'🔘Или нжмите <b>кнопку</b> из списка ниже.'
    photo = open('a8faeedd2789a1e54c18ce816645001c.jpeg', 'rb')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    button_list = ["77551", "77xxx","77xxx","77xxx"]
    keyboard.add(*button_list)
    await bot.send_photo(chat_id=message.from_user.id, photo=photo, caption=text, reply_markup=keyboard, parse_mode='html')

from fuctions import employees, sp, night


@dp.message_handler(lambda message: message.text == '77551')
async def azs(message: Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    button_list = [types.KeyboardButton(text=employees[x]) for x in range(len(employees))]
    keyboard.add(*button_list)
    text = f'👥Выберите себя в списке сотрудников, чтобы увидеть его календарь на текущий месяц!'
    await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=keyboard,
                         parse_mode='html')

from fuctions import chass, dnya, closest
import datetime as dt
from calendar import monthrange

@dp.message_handler(lambda message: message.text in employees)
async def emp(message: Message):
    for i in range(len(employees)):
        j = employees.index(message.text)
        # Выделяем даты из всех наименований списка
        long = monthrange(dt.datetime.now().year, dt.datetime.now().month)[1]
        days_only = dict(list(sp[j].items())[4:4+long])
        # Ищем даты только рабочие
        work_days = [key for key, value in days_only.items() if value != 'В' and value != 'ОТ']
        days_only_sorted = {k: days_only[k] for k in work_days if k in days_only}
        # Ищем рабочие часы - ночные
        night_only_sorted = {k: night[j][k] for k in work_days if k in night[j]}
        kluchi = list(days_only_sorted.keys())
        output_list_day = []
        znach = list(days_only_sorted.values())
        output_list_value = []
        # Создаем список из ключей со сменами с переходом на новый день
        i = 0
        while i < len(kluchi):
            if i < len(kluchi) - 1 and int(kluchi[i]) + 1 == int(kluchi[i + 1]):
                if i < len(kluchi) - 3 and int(kluchi[i + 2]) + 1 == int(kluchi[i + 3]):
                    output_list_day.append("С {} на {}".format(kluchi[i], kluchi[i + 1]))
                    output_list_day.append("С {} на {}".format(kluchi[i + 2], kluchi[i + 3]))
                    i += 4
                elif i < len(kluchi) - 2 and int(kluchi[i]) + 2 == int(kluchi[i + 2]):
                    if int(znach[i]) < int(znach[i+1]):
                        output_list_day.append(kluchi[i])
                        output_list_day.append("С {} на {}".format(kluchi[i+1], kluchi[i + 2]))
                        i += 3
                else:
                    output_list_day.append("С {} на {}".format(kluchi[i], kluchi[i + 1]))
                    i += 2
            else:
                output_list_day.append(kluchi[i])
                i += 1

        l = 0
        while l < len(kluchi):
            if l < len(kluchi) - 1 and int(kluchi[l]) + 1 == int(kluchi[l + 1]):
                if l < len(kluchi) - 3 and int(kluchi[l + 2]) + 1 == int(kluchi[l + 3]):
                    output_list_value.append(int(znach[l]) + int(znach[l + 1]))
                    output_list_value.append(int(znach[l + 2]) + int(znach[l + 3]))
                    l += 4
                elif l < len(kluchi) - 2 and int(kluchi[l]) + 2 == int(kluchi[l + 2]):
                    if int(znach[l]) < int(znach[l + 1]):
                        output_list_value.append(znach[l])
                        output_list_value.append(int(znach[l+1]) + int(znach[l + 2]))
                        l += 3
                else:
                    output_list_value.append(int(znach[l]) + int(znach[l + 1]))
                    l += 2
            else:
                output_list_value.append(znach[l])
                l += 1

        # Ночные часы
        noch = list(night_only_sorted.values())
        output_list_noch = [noch[0]]
        for i in range(1, len(noch)):
            if int(noch[i]) == 5 and int(noch[i - 1]) == 2:
                output_list_noch.append(int(noch[i]) + int(noch[i - 1]))
                output_list_noch.remove(noch[i - 1])
            else:
                output_list_noch.append((noch[i]))

        # Отпуск
        otpusk1 = [key for key, value in days_only.items() if value == 'ОТ']
        otpusk = []
        for i in otpusk1:
            otpusk.append(i.zfill(2))

        days_of_week = []
        year = dt.datetime.now().year
        month = dt.datetime.now().month
        weekdays = {0: 'ПН',
                    1: 'ВТ',
                    2: 'СР',
                    3: 'ЧТ',
                    4: 'ПТ',
                    5: 'СБ',
                    6: 'ВС'}
        days_of_week = [weekdays.get(dt.date(year,month,int(kluchi[0])).weekday())]

        for i in range(1, len(kluchi)):
            prev = dt.date(year, month, int(kluchi[i-1])).weekday()
            tek = dt.date(year, month, int(kluchi[i])).weekday()
            if prev + 1 == tek:
                days_of_week.pop(-1)
                days_of_week.append(f'{weekdays.get(prev)}/{weekdays.get(tek)}')

            else:
                days_of_week.append(weekdays.get(tek))

        mesitsi =["Января","Февраля","Марта","Апреля","Мая","Июня","Июля","Августа","Сентября","Октября","Ноября","Декабря"]

        today = dt.datetime.now().day
        texting = ''
        mark = []
        for i in output_list_day:
            if len(i) > 5:
                if today == int(i[2:4]):
                    mark.append('🔘')
                elif today < int(i[2:4]):
                    mark.append('🔴')
                elif today > int(i[2:4]):
                    mark.append('🟢')
            else:
                if today == int(i[0:2]):
                    mark.append('🔘')
                elif today < int(i[0:2]):
                    mark.append('🔴')
                elif today > int(i[0:2]):
                    mark.append('🟢')

        for i in range(len(output_list_day)):
            texting = texting + f'{mark[i]}<b>{output_list_day[i]} {mesitsi[month-1].lower()}</b> - <b>{output_list_value[i]} {chass(output_list_value[i])}</b> <i>({output_list_noch[i]} ночных)</i>\n'


        zp = float(int(sp[j]["Рабочьих"])-int(sp[j]["Ночных"])-int(sp[j]["Празнечные"]))*240.24 + float(sp[j]["Ночных"])*1.4*240.24 + float(sp[j]["Празнечные"])*480.48
        this_date = dt.datetime.now().day
        kluchi = list(map(int, kluchi))
        dop = [kluchi[0]]
        for i in range(1, len(kluchi)):
            if kluchi[i - 1] + 1 == kluchi[i]:
                dop.append(kluchi[i - 1])
            elif kluchi[-1] - 1 != kluchi[-2]:
                dop.append(kluchi[-1])
        next_work_day = closest(this_date, dop)
        if next_work_day != None:
            date_index = kluchi.index(next_work_day)
            hour_index = znach[date_index]
            if hour_index == 3:
                rab_day = 21
            else:
                rab_day = 9
            for_colculation_next = dt.datetime(year,month,next_work_day,rab_day)
            for_colculation_today = dt.datetime(year,month,dt.datetime.now().day,dt.datetime.now().hour, dt.datetime.now().minute)
            delta = for_colculation_next-for_colculation_today
            zero = ''
            if (delta.seconds%3600)//60 < 10:
                zero = '0'
            smena = f"<i>Статус: следующая смена</i> <b>{next_work_day} {mesitsi[month-1].lower()} (через {delta.days} {dnya(delta.days)} {delta.seconds//3600}:{zero}{(delta.seconds%3600)//60 })</b>"
            if dt.datetime.now().day in dop:
               smena = f"<b>Статус: сейчас на смене</b>"
            elif dt.datetime.now().hour < 9 and dt.datetime.now().day-1 in dop:
               smena = f"<b>Статус: сейчас на смене</b>"
            elif delta.days == 0:
                smena = f"<i>Статус: следующая смена</i> <b>{next_work_day} {mesitsi[month - 1].lower()} (через {delta.seconds // 3600}:{zero}{(delta.seconds % 3600) // 60})</b>"
        else:
            smena = f'<b>В этом месяце смен больше нет!</b>'

        text = f'ℹ️<b>Информация о смене работника на период с 1 по {long} {mesitsi[month-1].lower()} {year} на {dt.datetime.now().day}.{dt.datetime.now().month}.{dt.datetime.now().year} {dt.datetime.now().hour}:{dt.datetime.now().minute}</b>\n' \
               f'\n' \
               f'🖊<i>ФИО:</i> <b>{sp[j]["ФИО"]}</b>\n' \
               f'🛢<i>Профессия:</i> <b>{sp[j]["Профессия"]}</b>\n' \
               f'#️⃣<i>Табельный номер:</i> <b>{sp[j]["Табельный номер"]}</b>\n' \
               f'\n' \
               f'📍{smena}\n' \
               f'\n' \
               f'{texting}\n' \
               f'<u><b>ВСЕГО</b></u>\n' \
               f'📆Рабочих дней: <b>{sp[j]["Рабочий"]} {dnya(sp[j]["Рабочий"])}</b>\n' \
               f'⚫️Выходных дней: <b>{sp[j]["Выходной"]} {dnya(sp[j]["Выходной"])}</b>\n' \
               f'🟠Отпуск: <b>{sp[j]["Отпуска"]} {dnya(sp[j]["Отпуска"])}</b>\n' \
               f'\n' \
               f'⏱Рабочие часы: <b>{sp[j]["Рабочьих"]} {chass({sp[j]["Рабочьих"]})}</b>\n' \
               f'🌃Ночные часы: <b>{sp[j]["Ночных"]} {chass({sp[j]["Ночных"]})}</b>\n' \
               f'🎊Праздничные часы: <b>{sp[j]["Празнечные"]} {chass({sp[j]["Празнечные"]})}</b>\n' \
               f'\n' \
               f'💰Номинальная ЗП: <b>{round(zp,2)}</b>' \
               f'\n' \
               f'\n' \
               f'Для возврата в предыдущее меню введите ваш номер АЗС:' \


        now = dt.datetime.now()
        year = now.year
        month = now.month

        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
        cal = calendar.TextCalendar().formatmonth(year, month, w=3)

        x = cal.split('\n')
        x.pop(0)
        x[0] = x[0].title()

        sps = []
        for i in range(len(x)):
            sps.append(x[i].split())

        number_of_days_last = calendar.monthrange(year, month)[1]
        last_m = list(range(number_of_days_last - 6, number_of_days_last + 1))

        if len(sps[1]) < 7:
            prev = 7 - len(sps[1])
            sps[1] = last_m[7 - prev:] + sps[1]

        if [] in sps:
            sps.remove([])

        next_m = list(range(1, 7))

        if len(sps[-1]) < 7:
            nxt = 7 - len(sps[-1])
            sps[-1] = sps[-1] + next_m[:nxt]

        updated_calendar = []
        for row in sps:
            updated_row = []
            for item in row:
                updated_item = str(item).zfill(2)
                updated_row.append(updated_item)
            updated_calendar.append(updated_row)

        text1 = ''
        for i in updated_calendar:
            text1 += '   '.join(i) + '\n'

        # Создаем изображение календаря
        img = Image.new('RGB', (266, 145+35*len(updated_calendar)), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("/Users/artem/Downloads/Программы/Bot/ofont.ru_Futuris.ttf", 19 , encoding='utf-8')

        watermark = Image.open('LukOil-Logo-PNG-Clipart-Background.png')
        watermark_resized = watermark.resize((200, 52))
        img.paste(watermark_resized, (33, 15), watermark_resized)
        mon =["Январь","Февраль","Март","Апрель","Май","Июнь","Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь"]

        draw.text((49,71), f'{mon[month - 1].upper()} {year}', font=ImageFont.truetype("/Users/artem/Downloads/Программы/Bot/ofont.ru_Futuris.ttf", 22 , encoding='utf-8'), fill=(0,0,0))

        d = list(map(int, kluchi))
        today = dt.datetime.now().day
        dop1 = list(map(str, dop))

        for i in range(len(updated_calendar)):
            for j in range(7):
                # Дни недели
                if updated_calendar[i][j] in updated_calendar[0]:
                    col = (0, 0, 0)
                elif updated_calendar[i][j] in updated_calendar[1][j] and int(updated_calendar[i][j]) > 20:
                    col = (196,196,196)
                elif updated_calendar[i][j] in updated_calendar[-1][j] and int(updated_calendar[i][j]) < 10:
                    col = (196, 196, 196)
                # Рабочие дни
                elif int(updated_calendar[i][j]) in d:
                    if today == int(updated_calendar[i][j]):
                        if str(today-1) in dop1 and dt.datetime(year, month, today, 9) < dt.datetime(year,month,int(updated_calendar[i][j]),dt.datetime.now().hour):
                            col = (0, 205, 0)
                        else:
                            col = (255, 0, 0)
                    elif today < int(updated_calendar[i][j]):
                        col = (255, 0, 0)
                    else:
                        col = (0,205,0)
                # Отпуска
                elif updated_calendar[i][j] in otpusk:
                    col = (255,130,0)
                else:
                    col = (0,0,0)

                dobavim = updated_calendar[i][j]
                x = 35
                y = 35
                if str(today) == updated_calendar[i][j]:
                    draw.rectangle(((26+x*j)-20, (118+y*i)-20, (26+x*j)+20, (118+y*i)+20), fill='white', outline='red', width=5)
                draw.text((15+x*j, 110+y*i), dobavim, font=font, fill=col)

        # Пояснение к календарю
        draw.rectangle((22 - 3, (116+35*len(updated_calendar)) - 3, 22 + 3, (116+35*len(updated_calendar)) + 3), fill='white',
                       outline='red', width=2)
        draw.ellipse((22 - 3, (131+35*len(updated_calendar)) - 3, 22 + 3, (131+35*len(updated_calendar)) + 3), fill='red', width=2)
        draw.ellipse((133 - 3, (116+35*len(updated_calendar)) - 3, 133 + 3, (116+35*len(updated_calendar)) + 3), fill=(0,205,0), width=2)
        draw.ellipse((133 - 3, (131+35*len(updated_calendar)) - 3, 133 + 3, (131+35*len(updated_calendar)) + 3), fill='orange', width=2)

        draw.text((30, 116+35*len(updated_calendar)-6), f' - текущий день', font=ImageFont.truetype("/Users/artem/Downloads/Программы/Bot/ofont.ru_Futuris.ttf", 9 , encoding='utf-8'), fill=(0,0,0))
        draw.text((30, 131+35*len(updated_calendar)-6), f' - будущая смена', font=ImageFont.truetype("/Users/artem/Downloads/Программы/Bot/ofont.ru_Futuris.ttf", 9 , encoding='utf-8'), fill=(0,0,0))
        draw.text((138, 116+35*len(updated_calendar)-6), f' - отработанная смена', font=ImageFont.truetype("/Users/artem/Downloads/Программы/Bot/ofont.ru_Futuris.ttf", 9 , encoding='utf-8'), fill=(0,0,0))
        draw.text((138, 131+35*len(updated_calendar)-6), f' - отпуск', font=ImageFont.truetype("/Users/artem/Downloads/Программы/Bot/ofont.ru_Futuris.ttf", 9 , encoding='utf-8'), fill=(0,0,0))

        # Преобразуем изображение в байты
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Отправляем изображение пользователю
    keyword = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyword.add(types.KeyboardButton("77551"))
    await bot.send_message(chat_id=message.from_user.id, text=text, parse_mode='html', reply_markup=keyword)
    await message.answer_photo(buffer)


# # генерируем ключ
# key = '123'
# kkk = '111'
# # переменная для хранения флага правильного ключа
# correct_key = False
#
# # async def check_key(message):
# #     global correct_key
# #     if message.text == key:
# #         if correct_key:
# #             await greet_user(message)
# #         else:
# #             correct_key = True
# #             await greet_user(message)
# #     elif message.text != key:
# #         await process_age(message)
# #         await bot.register_next_step_handler(message, check_key)
#
# @dp.message_handler(lambda message: message.text == key)
# async def greet_user(message):
#     # отправляем приветственное сообщение
#     text = "Добро пожаловать! Выберите опцию из меню:"
#     # создаем кнопки для меню
#     menu = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#     menu.add(types.KeyboardButton("Опция 1"))
#     menu.add(types.KeyboardButton("Опция 2"))
#     menu.add(types.KeyboardButton("Опция 3"))
#     # отправляем меню пользователю
#     await message.reply(text=text, reply_markup=menu)
#
# async def check_key(message: types.Message):
#     # проверяем введенный ключ
#     if message.text == key:
#         # отправляем сообщение "Правильно!" и завершаем функцию
#         await greet_user(message)
#         return
#     else:
#         # отправляем сообщение об ошибке и запрашиваем ключ снова
#         await message.reply(f'❌Вы ввели неправильный пароль!\n'
#                          f'\n'
#                          f'Введите ключ доступа повторно:')
#         await bot.register_next_step_handler(message, check_key)
#
# # обработчик команды старта
# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
#     # запрашиваем ключ у пользователя
#     await message.reply("Введите ключ доступа:")
#     # ожидаем ответа от пользователя
#     await bot.register_next_step_handler(message, check_key)
#
# password = "my_password" # задаем пароль
#
# @dp.message_handler(lambda message: message.text == "Опция 1")
# async def without_puree(message: types.Message):
#     await bot.send_message(chat_id=message.from_user.id, text='itog')