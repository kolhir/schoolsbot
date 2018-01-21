# -*- coding: utf-8 -*-
import time
from datetime import datetime,date
schools =("s14","s30","s37")
klases=("10А","10В", "9Б", "9А", "10А Не химики", "10А Химики")
vlz_dict = {"s14":["10А Не химики", "10А Химики"],"s30":["10А","10В", "9Б", "9А",], "s37":["10А",]}
start = "начало"
end = "конец"

l = "schools/"


users={}#{
            #"14":[{},[]],
            #"30":[{"111":"10Б","222":"9Б","333":"10Б",},[123,124,127]], 
            #"37":[{},[]]
        #}

for sch in list(vlz_dict.keys()):#shc - список школ
    other = {sch:[{},[]]} 
    users.update(other)
    for kl in vlz_dict[sch]:     #kl - конкретный класс школы 
        f=open(l + sch + "/" + kl)
        ids=f.read()
        ids=list(map(int,ids.split()))
        ids = dict.fromkeys(ids, kl)
        users[sch][0].update(ids)
        f.close()
    f=open(l + sch + "/" + sch)
    ids=f.read()
    ids=list(map(int,ids.split()))
    users[sch][1] = ids

def whoIsHe(user_id):
    who = []
    not_klass = [i for l in schools for i in users[l][1]]
    if user_id in not_klass:
        for sch in list(vlz_dict.keys()):
            if user_id in users[sch][1]:
                who = [sch]
                return who
    else:
        for sch in list(vlz_dict.keys()):
            if user_id in users[sch][0]:
                who = [sch, users[sch][0][user_id]]
                return who 
    return who

def addInSchool(user_id, school):
    users[school][1].append(user_id)
    f = open(l + school + "/" + school,'a')
    f.write(str(user_id) + ' ')

def addUser(user_id, klass, school):
#Добавляем в файл класса
    f = open((l+school+ "/" + klass),'a')
    f.write(str(user_id) + ' ')
    ids = {user_id:klass}
    users[school][0].update(ids)
    f.close()
#Удаляем из файла для тех, у кого нет класса  
    f = open((l+school+ "/" + school))
    ids = f.read()
    ids = list(map(int,ids.split()))
    ids.remove(user_id)
    f.close()  
    f = open((l+school+ "/" + school),'w')
    for i in ids: f.write(str(i)+' ')
    f.close()
    users[school][1].remove(user_id)

def deleteUserFromKlass(user_id):
    s = whoIsHe(user_id)
    if (len(s) == 2):

        klass = s[1]
        school = s[0]
        f= open((l+school+ "/" + klass))#TODO
        ids=f.read()
        ids = list(map(int,ids.split()))
        ids.remove(user_id)
        f.close()

        f = open((l+school+ "/" + klass),'w')
        for i in ids: f.write(str(i)+' ')
        f.close()
        users[school][0].pop(user_id)

        f= open((l+school+ "/" + school), 'w')
        f.write(str(user_id) + ' ')
        f.close()
        users[school][1].append(user_id)
    
def deleteUser(user_id):
    s = whoIsHe(user_id)
    
    print(2)
    if len(s) == 2:
        klass = s[1]
        school = s[0]
        f= open((l+school+ "/" + klass))#TODO
        ids=f.read()
        ids = list(map(int,ids.split()))
        ids.remove(user_id)

        f = open((l+school+ "/" + klass),'w')
        for i in ids: f.write(str(i)+' ')
        f.close()
        users[school][0].pop(user_id)

    elif len(s) == 1:
        school = s[0]
        f = open((l+school+ "/" + school))
        ids = f.read()
        ids = list(map(int,ids.split()))
        ids.remove(user_id)
        f.close()  
        f = open((l+school+ "/" + school),'w')
        for i in ids: f.write(str(i)+' ')
        f.close()
        users[school][1].remove(user_id)

def nextLesson(usList):

    school = usList[0]
    klass = usList[1]
    if school == "s14":
        from schools.s14.config import tt, timeles
    elif school == "s30":
        from schools.s30.config import tt, timeles
    elif school == "s37":
        from schools.s37.config import tt, timeles

    timenow = time.strptime(time.strftime("%X", time.localtime()), "%X")
    weekday_number = date.weekday(datetime.now())
    weekdays=("Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье")
    day = weekdays[weekday_number]
    answer=""
    flag = ""
    if weekday_number == 6:
        answer = "А сегодня не воскресенье???"
        return answer
    elif weekday_number == 5:
        w = 1
    else: w = 0
    if not(tt[klass][day]):
        answer = "Так хочется учиться сегодня??? Сорри, кажется у тебя сегодня выходной."
        return answer
    # print("tt = ", tt, "\n", "tt[klass] =", tt[klass], "\n", "tt[klass][day] =" , tt[klass][day])
    for i in range(1,10):
        start1b = time.strptime(timeles[w][start][str(i)], "%X")
        start1e = time.strptime(timeles[w][end][str(i)], "%X")
        start2b = time.strptime(timeles[w][start][str(i + 1)], "%X") 
        start2e = time.strptime(timeles[w][end][str(i + 1)], "%X")
        # if  (i == 1) and (timenow < start1b):
        #     answer = ("Следующий урок: "+ str(tt[klass][day][str(i)]))
        #     flag = str( tt[klass][day][str(i+1)])
        #     break
        if start1b <= timenow <=  start1e:
            answer = ("Следующий урок: "+ str(tt[klass][day][str(i+1)]))
            flag = str( tt[klass][day][str(i+1)])
            break
        elif start1e <= timenow <= start2b:
            answer = ("Уже скоро начнется: " + str(tt[klass][day][str(i+1)]))
            flag = str(tt[klass][day][str(i+1)])
            break
        elif (i == 9) and (start2b <= timenow <= start2e):
            answer = ("Сейчас идет последний урок")
            flag = str(tt[klass][day][str(i+1)])
            break
        elif (i == 9) and (timenow > start2e):
            answer = ("Все, остановись, сегодня больше нет уроков")
            flag = str(tt[klass][day][str(i+1)])
            break
        elif (i==1) and (timenow < start1b):
            if (tt[klass][day]):
                for k in range(1,10):
                    if (tt[klass][day][str(k)]):
                        answer = ("Следующий урок: "+ str(tt[klass][day][str(k)]))
                        flag = str(tt[klass][day][str(k)])
                        break
            else:  
                answer = "Сегодня нет уроков"
                flag = "1"
                break 
    if flag:
        return answer
    else:
        answer = "Сегодня больше нет уроков"
        return answer

def onDay(day, usList):
    school = usList[0]
    klass = usList[1]
    if school == "s14":
        from schools.s14.config import tt, timeles
    elif school == "s30":
        from schools.s30.config import tt, timeles
    elif school == "s37":
        from schools.s37.config import tt, timeles
    answer = ""
    flag = 0
    win = ""

    if day != "Суббота":
        w = 0
    else: w = 1

    if not(tt[klass][day]):
        answer = ("Ты разве учишься в этот день?!")
        return answer

    for i in range(1,11):
        st = str(timeles[w][start][str(i)])
        en = str(timeles[w][end][str(i)])
        if (tt[klass][day][str(i)] == ""):
            win = win + (str(i) + ". " + st[0:5] + " - " +en[0:5]+ " " + str(tt[klass][day][str(i)]) + " \n")
            flag = flag + 1
        else:
           answer = answer + win + (str(i) + ". " + st[0:5] + " - " +en[0:5]+ " " + str(tt[klass][day][str(i)]) + " \n")
           win = ""
        if ((i == 10) and (flag == 10)) or not(tt[klass][day]):
            answer = ("Вы не учитесь в этот день")
            break   
    return answer

def untilTheEnd(usList):
    def deltaplan(now_time, next_time):
        answer=0
        (now_time,next_time)=(list(now_time),list(next_time))
        if now_time[3]>next_time[3] :next_time[3]=next_time[3]+24
        if now_time[5]>next_time[5] :answer=answer-1
        answer=answer+(next_time[3]-now_time[3])*60+next_time[4]-now_time[4]
        return answer

    def valMinute(delta):
        answer = ""
        if delta<=2:
            answer = ("До конца урока осталось совсем чуть-чуть:)")
        elif 11 <= delta <= 19:
            answer = ("До конца урока осталось: " + str(delta) + " минут" )
        elif delta % 10 == 1: 
            answer = ("До конца урока осталось: " + str(delta) + " минутa" )
        elif 2 <= (delta % 10) <= 4:
            answer = ("До конца урока осталось: " + str(delta) + " минуты" )
        else:
            answer = ("До конца урока осталось: " + str(delta) + " минут" )
        return answer

    def minute(delta):
        answer = ""
        if 11 <= delta <= 19:
            answer = (" минут" )
        elif delta % 10 == 1: 
            answer = (" минутa" )
        elif 2 <= (delta % 10) <= 4:
            answer = (" минуты" )
        else:
            answer = (" минут" )
        return answer
        
    school = usList[0]
    klass = usList[1]

    if school == "s14":
        from schools.s14.config import tt, timeles
    elif school == "s30":
        from schools.s30.config import tt, timeles
    elif school == "s37":
        from schools.s37.config import tt, timeles

    timenow = time.strptime(time.strftime("%X", time.localtime()), "%X")
    weekday_number = date.weekday(datetime.now())
    weekdays=("Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье")
    day = weekdays[weekday_number]
    answer=""
    flag = ""

    if weekday_number == 6:
        answer = "Show must go on"
        return answer
    elif weekday_number == 5:
        w = 1
    else: w = 0

    if not(tt[klass][day]):
        answer = ("Ты разве учишься сегодня?!")
        return answer

    for i in range(1,10):
        start1b = time.strptime(timeles[w][start][str(i)], "%X")
        start1e = time.strptime(timeles[w][end][str(i)], "%X")
        start2b = time.strptime(timeles[w][start][str(i + 1)], "%X") 
        start2e = time.strptime(timeles[w][end][str(i + 1)], "%X")
        if start1b <= timenow <=  start1e:
            if str(tt[klass][day][str(i)]):
                delta = deltaplan(timenow, start1e)
                answer = valMinute(delta)
                break
        elif start1e <= timenow <= start2b:
            if str(tt[klass][day][str(i+1)]):
                delta = deltaplan(timenow, start2b)
                answer = ("Сейчас перемена!\nДо начала урока : " + str(delta) + minute(delta))
                break
        elif (i == 9) and (start2b <= timenow <= start2e):
            if str(tt[klass][day][str(i)]):
                delta = deltaplan(timenow, start1e)
                answer = valMinute(delta)      
                break   
        else:
            answer = ("Ой все, отстань")
    return answer