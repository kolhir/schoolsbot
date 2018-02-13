import telebot, config, time, random,copy
import func as f
from somewhere import admins
stat = copy.deepcopy(config.stat_update)
token = config.token
bot = telebot.TeleBot(token, threaded=False)
# bot = telebot.TeleBot(token)
weekdays=("Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье")
def stat_on_day(message,flag):
    global stat
    try:
        if len(flag) == 2:
            if not(message.from_user.id in stat["school"][flag[0]][flag[1]]):
                stat["school"][flag[0]][flag[1]].append(message.from_user.id)

    except Exception as e:
        print("Ошибка статистики 1 ", e)

    if (message.text in config.list_command) or (message.text in weekdays):
        try:
            stat[message.text]
        except Exception as e:
            stat[message.text] = []
        if not(message.from_user.id in stat[message.text]):
            stat[message.text].append(message.from_user.id)
    else:
        try:
            dv = {message.text:message.from_user.id}
            stat["not_know"].update(dv)
        except Exception as e:
            print("Ошибка статистики 2 ", e)

def rand_quote(message):
    rand = (random.randint(0,37))
    # if  (0 < rand <= 37):
    quote = config.quote[rand]
    timenow = time.strftime("%X", time.localtime())
    k = message.from_user
    l = f.whoIsHe(k.id)
    print("Вывод")
    if(len(l) == 2):
        print("Школа: ",l[0], "; Класс: ", l[1], "; Время: ", timenow, sep = "")
    print(k.id, ";  Имя: ", k.first_name, ";  Фамилия: ", k.last_name, "; User_name: ", k.username, "\n", "Отправлена цитата:", quote , "\n", sep = "")
    bot.send_message(message.from_user.id, quote , start_murkup())

def my_send_message(userid, string, user_markup, message):
    l = f.whoIsHe(userid)
    timenow = time.strftime("%X", time.localtime())
    k = message.from_user
    print("Вывод")
    if(len(l) == 2):
        print("Школа: ",l[0], "; Класс: ", l[1], "; Время: ", timenow, sep = "")
    print(k.id, ";  Имя: ", k.first_name, ";  Фамилия: ", k.last_name, "; User_name: ", k.username, "\n", "Сообщение: ", string, "\n", sep = "")
    return (bot.send_message(userid, string, reply_markup = user_markup))

def my_send_message_WK(userid, string, message):
    k = message.from_user
    l = f.whoIsHe(userid)
    timenow = time.strftime("%X", time.localtime())
    k = message.from_user
    print("Вывод")
    if(len(l) == 2):
        print("Школа: ",l[0], "Класс: ", l[1], "Время: ", timenow, sep = "")
    print(k.id, "; Имя: ", k.first_name, "; Фамилия: ", k.last_name, "; User_name: ", k.username, "\n", "Сообщение: ", string, "\n", sep = "")
    return (bot.send_message(userid, string))

def start_murkup():
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Следующий урок')
    user_markup.row('Расписание на день')
    user_markup.row('Сколько осталось до звонка?')
    user_markup.row('Изменить что-нибудь')
    return user_markup

def choose_school(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    for i in f.schools:
        user_markup.row(i[1:])
    user_school = my_send_message(message.from_user.id, "Выбери школу", user_markup, message)

def choose_klass(message):
    l = f.whoIsHe(message.from_user.id)
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    if (len(l) == 1):
        for i in f.vlz_dict[l[0]]:
            user_markup.row(i)
    user_markup.row("Изменить школу")
    user_klass = my_send_message(message.from_user.id, "Выбери класс", user_markup, message)

def start(message):
    my_send_message(message.from_user.id, "Выбери действие",  start_murkup(), message)

def ttOnDay(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Понедельник', 'Четверг')
    user_markup.row('Вторник', 'Пятница')
    user_markup.row('Среда', 'Суббота')
    day = my_send_message(message.from_user.id, "Выбери день", user_markup, message)
    bot.register_next_step_handler(day, onDay)

def change_smt(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Изменить класс')
    user_markup.row('Изменить школу')
    my_send_message(message.from_user.id, "Что изменить?", user_markup, message)

def nextLesson(message):
    answer = f.nextLesson(f.whoIsHe(message.from_user.id))
    if answer == "":
        rand_quote(message)
    else:
        my_send_message(message.from_user.id, answer, start_murkup(), message)###Передать класс человека
        if answer in config.not_lesson:
            rand_quote(message)

def untilTheEnd(message):
    answer =  f.untilTheEnd(f.whoIsHe(message.from_user.id))
    if answer == "":
        rand_quote(message)
    else:
        my_send_message(message.from_user.id, answer, start_murkup() ,message)###Передать класс человека
        if answer in config.not_lesson:
            rand_quote(message)

@bot.message_handler(commands=['start'])
def handle_start(message):
    flag = f.whoIsHe(message.from_user.id)
    stat_on_day(message,flag)
    if not(flag):
        choose_school(message)
    else:
        start(message)

@bot.message_handler(commands=['stat'])
def handle_stat(message):
    if message.from_user.id in admins:
        s = ""
        k = []
        for i in stat["school"].keys():
            for ii in stat["school"][i]:
                s = s + (i + " : " + ii + " : " + str(len(stat["school"][i][ii])) + "\n")
                k = k + stat["school"][i][ii]
        all_users = []
        for i in k:
            if not(i in all_users):
                all_users.append(i)
        s = s + ("Всего пользователей: " + str(len(all_users)) + "\n")
        for i in list(stat.keys())[1:]:
            s = s + (i + " : " + str(len(stat[i])) + "\n")
        bot.send_message(message.from_user.id, s)

    else:
        s = "Кажется ты не админ 😱"
        bot.my_send_message(message.from_user.id, s, start_murkup(), message)

@bot.message_handler(commands=['notknow'])
def handle_notknow(message):
    if message.from_user.id in admins:
        s = ""
        for i in stat["not_know"]:
            s = s + (str(i) + " : " + str(stat["not_know"][i]) + "\n")
        bot.send_message(message.from_user.id, s)
    else:
        s = "Кажется ты не админ 😱"
        bot.my_send_message(message.from_user.id, s, start_murkup(), message)

@bot.message_handler(commands=['statupdate'])
def handle_statupdate(message):
    if message.from_user.id in admins:
        global stat
        stat =copy.deepcopy(config.stat_update)
        s = "Готово"
        bot.send_message(message.from_user.id, s)
    else:
        s = "Кажется ты не админ 😱"
        bot.my_send_message(message.from_user.id, s, start_murkup(), message)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    l = f.whoIsHe(message.from_user.id)
    timenow = time.strftime("%X", time.localtime())
    k = message.from_user
    stat_on_day(message,l)
    print("Ввод")
    if(len(l) == 2):
        print("Школа: ",l[0], "; Класс: ", l[1], "; Время: ", timenow, sep = "")
    elif(len(l) == 1):
        print("Школа: ",l[0], "; Время: ", timenow, sep = "")
    print(k.id, ";  Имя: ", k.first_name, ";  Фамилия: ", k.last_name, "; User_name: ", k.username, "\n", "Сообщение от пользователя: ", message.text, "\n", sep = "")

    if len(l) == 2:
        if message.text == "Следующий урок":
            nextLesson(message)
        elif message.text == "Расписание на день":
            ttOnDay(message)
        elif message.text == "Сколько осталось до звонка?":
            untilTheEnd(message)
        elif message.text == "Изменить что-нибудь":
            change_smt(message)
        elif message.text == "Изменить класс":
            f.deleteUserFromKlass(message.from_user.id)
            choose_klass(message)
        elif message.text == "Изменить школу":
            f.deleteUser(message.from_user.id)
            choose_school(message)
        else: start(message)
    elif (len(l) == 1) and (message.text == "Изменить школу"):
        f.deleteUser(message.from_user.id)
        choose_school(message)
    elif ("s"+message.text) in f.schools:
        message.text = "s" + message.text
        if len(l) == 0:
            f.addInSchool(message.from_user.id, message.text)
            choose_klass(message)
        elif len(l) == 1:
            choose_klass(message)
        else:
            start(message)

    elif message.text in f.klases:
        if len(l) == 0:
            choose_school(message)
        elif len(l) == 1:
            f.addUser(message.from_user.id, message.text, l[0])
        start(message)
    elif len(l) == 1:
        choose_klass(message)
    else:
        choose_school(message)

def onDay(message):
    stat_on_day(message,f.whoIsHe(message.from_user.id))
    if message.text in weekdays:
        print(message.text)
        answer = f.onDay(message.text, f.whoIsHe(message.from_user.id))
        if answer == "":
            rand_quote(message)
        else:
            my_send_message(message.from_user.id, answer, start_murkup(), message)###Передать класс человека
            if answer in config.not_lesson:
                rand_quote(message)
    elif message.text == "Следующий урок":
        nextLesson(message)
    else: ttOnDay(message)
while True:

    try:
        bot.polling(none_stop=True)

    except Exception as e:
        print("Ошибка: ",e)
        import traceback; traceback.print_exc()  # или просто print(e) если у вас логгера нет,
        # или import traceback; traceback.print_exc() для печати полной инфы
        time.sleep(15)
