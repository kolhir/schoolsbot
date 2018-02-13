import config, telebot
token = config.token
bot = telebot.TeleBot(token)

s = ""
s30 = ""
s14 = ""
s37 = ""

l30 = ["9А", "9Б", "10А","10В"]
l37 = ["10А"]
l14 = ["10А Не химики", "10А Химики"]

d = {"s30":[],"s37":[],"s14":[]}

for i in l30:
    f = open("schools/s30/" + i,"r")
    s30 = s30 + f.read()
d["s30"] = s30.split()

for i in l37:
    f = open("schools/s37/" + i,"r")
    s37 = s37 + f.read()
d["s37"] = s37.split()

for i in l14:
    f = open("schools/s14/" + i,"r")
    s14 = s14 + f.read()

d["s14"] = s14.split()


for key in d:
    print(len(d[key]))
    for i in d[key]:
        try:
            # print(key, i, sep = " : ")
            # bot.send_message(i, "Просим прощения, но бот не будет работать до завтрашнего вечера, по причине пенеоса его к более стабильному электричеству и интернету.\nСпасибо за понимание. \nНе скучайте😊")
        except Exception as e:
            print(i, "Не отправлено")
        else:
            print(i, "Отправлено")
