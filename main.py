import requests
import schedule
import time
from bs4 import BeautifulSoup
import telebot
import random
import sqlite3
import threading
from parses import *
from database import *
mama = ["жива","мертва"]
BOT = telebot.TeleBot("5217412431:AAHPCZSije457hOGE7ow4CNAAnCVOLWBFzk")
user_data = {}

__connection = None


def getid(name):
    if type(name) == tuple or type(name) == list:
        print(name)
        name = name[-1]
    headers = {
        "user-agent": "Mozilla/5.0 (Windows; U; Windows 95) AppleWebKit/531.36.1 (KHTML, like Gecko) Version/4.1 Safari/531.36.1"}
    req = requests.get("https://steamid.xyz/" + name, headers=headers)
    reques = req.text
    soup = BeautifulSoup(reques, "lxml")
    try:
        id = soup.find("div", id="guide").find("input", type = "text").find_next().find_next()["value"]
    except AttributeError:
        id = False
    return(id)

def parse(id):
    link = f"https://www.dotabuff.com/players/{id}"
    headers = {"user-agent" : "Mozilla/5.0 (Windows; U; Windows 95) AppleWebKit/531.36.1 (KHTML, like Gecko) Version/4.1 Safari/531.36.1"}
    req = requests.get(link, headers = headers)
    reques = req.text
    soup = BeautifulSoup(reques, "lxml")
    try:
        soup.find("div", class_="header-content-container").find("dl").next_element.next_element.next_element.next_element.text

    except AttributeError:
        return False

    wins = soup.find("div", class_="header-content-container").find("dl").next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.text
    loses = soup.find("div", class_="header-content-container").find("dl").next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.text
    wr = soup.find("div", class_="header-content-container").find("dl").next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.text
    rank = soup.find("div", class_="header-content-container").find("div", class_ = "header-content").find("div", class_ = "header-content-secondary").find("div", class_="rank-tier-wrapper")["title"][6:]
    role = soup.find("div", class_="row-12 with-sidebar player-summary").find("div", class_ = "role-chart").find("div", class_ = "roles bar").find("div", class_ = "lane-group").find("div", class_ = "r-none-mobile").text.strip()
    signature_heroes = soup.find("div", class_="r-table r-only-mobile-5 heroes-overview").find_all("div", class_ = "r-row")

    heroes = []
    heroes_winrate = []

    for x in signature_heroes:
        heroes.append(x.find("div", class_ = "r-fluid r-35 r-icon-text").find("div", class_ = "r-body").find("div", class_ = "r-none-mobile").find("a").text)
        heroes_winrate.append(x.find("div", class_ = "r-fluid r-10 r-line-graph").next_element.next_element.next_element.next_element.next_element.next_element.next_element.find("div", class_ = "r-body").text)

    dic = dict(zip(heroes, heroes_winrate))
    a = (f"""
Wins = {wins}

Loses = {loses}

WinRate = {wr}

Rank = {rank}

Role = {role}

Heroes = 
    """)
    for x in dic:
        a += f"""
{x} {dic[x]}
"""
    return a


def get_meta(pos):
        link = "https://dota2protracker.com/meta"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows; U; Windows 95) AppleWebKit/531.36.1 (KHTML, like Gecko) Version/4.1 Safari/531.36.1"}
        req = requests.get(link, headers=headers)
        reques = req.text
        soup = BeautifulSoup(reques, "lxml")
        if pos > 0:
            heroes1 = soup.find("div", class_ = f"content-box tabs-{pos + 1} inactive").find_all("div", class_ = "top-hero")
        else:
            heroes1 = soup.find("div", class_ = "content-box tabs-1 active").find_all("div", class_ = "top-hero")
        heroes = []
        winrate = []
        for x in heroes1:
            heroes.append(x.find("div", class_ = "top-hero-head").find("a")["title"])
            winrate.append(x.find("div", class_ = "top-hero-body").find("div", class_ = "top-hero-stat").find("span").text)
        print(heroes, winrate)
        dicti = dict(zip(heroes, winrate))
        a = (""" 
            """)
        for x in dicti:
            a += f"""
{x} {dicti[x]} 
"""
        return a


def getname(name):
    if type(name) == tuple or type(name) == list:
        print(name)
        name = name[-1]
    headers = {
        "user-agent": "Mozilla/5.0 (Windows; U; Windows 95) AppleWebKit/531.36.1 (KHTML, like Gecko) Version/4.1 Safari/531.36.1"}
    req = requests.get("https://steamid.xyz/" + name, headers=headers)
    reques = req.text
    soup = BeautifulSoup(reques, "lxml")
    try:
        id = soup.find("div", id="guide").find("input", type = "text").find_next().find_next().find_next().find_next()["value"]
    except AttributeError:
        id = False
    return(id)


def check_last_game(id):
    id = str(id)
    ans = []
    link = f"https://www.dotabuff.com/players/{id}"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows; U; Windows 95) AppleWebKit/531.36.1 (KHTML, like Gecko) Version/4.1 Safari/531.36.1"}
    req = requests.get(link, headers=headers)
    reques = req.text
    soup = BeautifulSoup(reques, "lxml")
    lin = "https://www.dotabuff.com" + soup.find("div", class_="r-table r-only-mobile-5 performances-overview").find("div", class_="r-row").find("div", class_="r-fluid r-175 r-text-only r-right r-match-result").find("div", class_="r-body").find("a")["href"]
    req1 = requests.get(lin, headers=headers)
    reques1 = req1.text
    soup1 = BeautifulSoup(reques1, "lxml")
    vari = []
    vari.append("col-hints faction-radiant player-" + id)
    vari.append("col-hints faction-dire player-" + id)
    for x in vari:
        if soup1.find(class_ = x):
            her = soup1.find(class_ = x)
            break
    if len(her) < 1:
        her = ""
    try:
        her.find("td", class_="tf-pl single-lines").find("div", class_="subtext tf-inline").find(class_="lane-outcome").text
    except ValueError:
        ans.append(False)
    lane_status = her.find("td", class_="tf-pl single-lines").find("div", class_="subtext tf-inline").find(class_="lane-outcome").text
    if "Ranked" in (soup.find("div", class_="r-table r-only-mobile-5 performances-overview").find("div", class_="r-row").find("div", class_="r-fluid r-175 r-text-only r-first").find("div", class_="r-body").text):
        lg_stat = soup.find("div", class_="r-table r-only-mobile-5 performances-overview").find("div", class_="r-row").find("div", class_="r-fluid r-175 r-text-only r-right r-match-result").find("div", class_="r-body").find("a")["class"][-1]
        rank = 1
    else:
        lg_stat = 0
    if "Solo" in soup.find("div", class_="r-table r-only-mobile-5 performances-overview").find("div", class_="r-row").find("div", class_="r-fluid r-175 r-text-only r-first").find("i")["title"]:
        solo_check = "solo"
    elif "Party" in soup.find("div", class_="r-table r-only-mobile-5 performances-overview").find("div", class_="r-row").find("div", class_="r-fluid r-175 r-text-only r-first").find("i")["title"]:
        solo_check = "party"
    ans.append(lane_status)
    ans.append(lin)
    ans.append(rank)
    ans.append(solo_check)
    ans.append(str(lg_stat))
    return ans



def get_conection():
    global __connection
    if __connection is None:
        __connection = sqlite3.connect("bot.db", check_same_thread = False)
    return __connection


def init_db(force: bool = False):
    conn = get_conection()
    c = conn.cursor()
    if force:
        c.execute("DROP TABLE IF EXISTS bot")

    c.execute("""
            CREATE TABLE IF NOT EXISTS bot(
                id          INTEGER PRIMARY KEY,
                user_id     INTEGER NOT NULL,
                dotabuff_id TEXT NOT NULL,
                sub_status  BOOLEAN,
                total_day   INTEGER,
                last_game   INTEGER     
        )
    """)
    conn.commit()


def add_dbid(user_id: int, dotabuff_id: str):
    conn = get_conection()
    c = conn.cursor()
    c.execute("INSERT INTO bot (user_id, dotabuff_id) VALUES (?, ?)", (user_id, dotabuff_id))
    conn.commit()


def checkreg(user_id = int):
    conn = get_conection()
    c = conn.cursor()
    inf = c.execute("SELECT * FROM bot WHERE user_id=?", (user_id, ))
    if inf.fetchone() is None:
        return True
    else:
        return False


def myprofile(user_id = int):
    conn = get_conection()
    c = conn.cursor()
    c.execute("SELECT dotabuff_id FROM bot WHERE user_id = ?", (user_id,))
    res = c.fetchone()
    conn.commit()
    return(res)


def del_user(user_id = int):
    conn = get_conection()
    c = conn.cursor()
    c.execute("DELETE FROM bot WHERE user_id = ?", (user_id,))
    conn.commit()

def edit_sub(user_id: int, subscribe = bool):
    conn = get_conection()
    c = conn.cursor()
    c.execute("UPDATE bot SET sub_status = ? WHERE user_id = ?", (user_id, subscribe))
    conn.commit()


def get_subscribtions(sub_status):
    conn = get_conection()
    c = conn.cursor()
    c.execute("SELECT user_id FROM bot WHERE sub_status = 1")
    res = c.fetchall()
    conn.commit()
    return(res)


def get_last_game(dotabuff_id):
    conn = get_conection()
    c = conn.cursor()
    c.execute("SELECT last_game FROM bot WHERE dotabuff_id = ?", (dotabuff_id,))
    res = c.fetchone()
    conn.commit()
    return (res)



def edit_last_game(dotabuff_id, last_game):
    conn = get_conection()
    c = conn.cursor()
    c.execute("UPDATE bot SET last_game = ? WHERE dotabuff_id = ?", (last_game, dotabuff_id))
    conn.commit()

def edit_rating_plus_solo(dotabuff_id):
    conn = get_conection()
    c = conn.cursor()
    c.execute("UPDATE bot SET total_day = total_day + 30 WHERE dotabuff_id = ?", (dotabuff_id, ))
    conn.commit()

def edit_rating_minus_solo(dotabuff_id):
    conn = get_conection()
    c = conn.cursor()
    c.execute("UPDATE bot SET total_day = total_day - 30 WHERE dotabuff_id = ?", (dotabuff_id, ))
    conn.commit()


def get_total_day(dotabuff_id):
    conn = get_conection()
    c = conn.cursor()
    c.execute("SELECT total_day FROM bot WHERE dotabuff_id = ?", (dotabuff_id,))
    res = c.fetchone()
    conn.commit()
    return (res)

def edit_rating_zero(dotabuff_id):
    conn = get_conection()
    c = conn.cursor()
    c.execute("UPDATE bot SET total_day = 0 WHERE dotabuff_id = ?", (dotabuff_id, ))
    conn.commit()

def edit_rating_plus_party(dotabuff_id):
    conn = get_conection()
    c = conn.cursor()
    c.execute("UPDATE bot SET total_day = total_day + 20 WHERE dotabuff_id = ?", (dotabuff_id, ))
    conn.commit()

def edit_rating_minus_party(dotabuff_id):
    conn = get_conection()
    c = conn.cursor()
    c.execute("UPDATE bot SET total_day = total_day - 20 WHERE dotabuff_id = ?", (dotabuff_id, ))
    conn.commit()


def startbot():
    BOT.polling(none_stop=True)


def runScheluders():
    schedule.every(10).minutes.do(spam)

def ScheludeDay():
    schedule.every().day.at("16:11").do(daynoti)


def daynoti():
    al = get_subscribtions(1)
    subs1 = []
    for x in range(len(al)):
        subs1.append(al[x][0])
    subs = [str(i) for i in subs1]
    dbids = []
    for x in subs:
        a = myprofile(x)
        dbids.append(str(a[0]))
    for x in dbids:
        a = get_total_day(x)[0]
        if a < 0:
            BOT.send_message(subs[dbids.index(x)], f"К сожалению, за день ты ушел в минус на {abs(a)} mmr, завтра отыграешься")
        elif a > 0:
            BOT.send_message(subs[dbids.index(x)], f"Сегодня ты в плюсе на {a} mmr, хорош")
        else:
            BOT.send_message(subs[dbids.index(x)], f"За сегодня ты в нуле, не слил-уже хорошо")

def spam():
    print(get_subscribtions(1))
    al = get_subscribtions(1)
    subs1 = []
    for x in range(len(al)):
        subs1.append(al[x][0])
    subs = [str(i) for i in subs1]
    print(subs)
    dbids = []
    for x in subs:
        a = myprofile(x)
        dbids.append(str(a[0]))
    print(dbids)
    for x in dbids:
        v = check_last_game(x)
        if get_last_game(x)[0] != None:
            edit_last_game(x,v[1])
        elif get_last_game(x)[0] != v[1]:
            if v[0] != None:
                if v[0] == "won":
                    BOT.send_message(subs[dbids.index(x)], "Хорош, разьебал лайн в ласт катке")
                elif v[0] == "drew":
                    BOT.send_message(subs[dbids.index(x)], "Потный лайн был, но ты молодец, отстоял ровно")
                else:
                    BOT.send_message(subs[dbids.index(x)], "Лайн проёбан, но жизнь продолжается!)")

                edit_last_game(x, v[1])
                if get_total_day(x)[0] == None:
                    edit_rating_zero(x)
                else:
                    if v[2] == 1:
                        if v[-1] == "won":
                            if v[3] == "solo":
                                edit_rating_plus_solo(x)
                            elif v[3] == "party":
                                edit_rating_plus_party(x)
                        elif v[-1] == "lost":
                            if v[3] == "solo":
                                edit_rating_minus_solo(x)
                            elif v[3] == "party":
                                edit_rating_minus_party(x)




@BOT.message_handler(commands = ["unreg","regdel", "delreg"])
def delreg(message):
    if checkreg(message.from_user.id) == False:
        del_user(message.from_user.id)
        BOT.send_message(message.chat.id, "Ваш профиль удалён из базы данных")
    else:
        BOT.send_message(message.chat.id, "За вами не закреплено аккаунта")



@BOT.message_handler(commands = ["asdf"])
def reg(message):
    spam()
@BOT.message_handler(commands = ["register","reg"])
def reg(message):
    msg = message.text.split()
    if len(msg) == 1:
        BOT.send_message(message.chat.id, "Введи /reg ссылка/id_профиля")
    else:
        dot = getid(msg)
        if dot != False:
            if checkreg(message.from_user.id) == True:
                init_db()
                add_dbid(user_id=message.from_user.id, dotabuff_id=dot)
                BOT.send_message(message.chat.id, "Вы успешно зарегестрированы!")
            else:
                BOT.send_message(message.chat.id, "Вы уже зарегестрированы")
        else:
            BOT.send_message(message.chat.id, "Чёто не то ввёл")


@BOT.message_handler(commands = ["info"])
def info(message):
    BOT.send_message(message.chat.id, """
Чекнуть профиль - по кнопке, или команда /check и id
Мой профиль - регистрация своего аккаунта
Если чёто не так с регистрацией - /delreg или /unreg
Чекнуть мать - если не пусси жми
Соси хуй
    """)


@BOT.message_handler(commands = ["check"])
def info(message):
    if len(message.text.split()) > 1:
        acc = message.text.split()[-1]
        if acc.startswith("https://steamcommunity.com/id/"):
            if acc[-1] == "/":
                name = acc.replace("https://steamcommunity.com/id/", "")
                name = name[:-1]
                a = parse(getid(name))
                if a == False:
                    BOT.send_message(message.chat.id, "Такого аккаунта нет на дотабаффе")
                else:
                    BOT.send_message(message.chat.id, a)
            else:
                name = acc.replace("https://steamcommunity.com/id/", "")
                a = parse(getid(name))
                if a == False:
                    BOT.send_message(message.chat.id, "Такого аккаунта нет на дотабаффе")
                else:
                    BOT.send_message(message.chat.id, a)
        elif acc.startswith("http://steamcommunity.com/profiles/"):
            if acc[-1] == "/":
                name = acc.replace("http://steamcommunity.com/profiles/", "")
                name = name[:-1]
                a = parse(getid(name))
                if a == False:
                    BOT.send_message(message.chat.id, "Такого аккаунта нет на дотабаффе")
                else:
                    BOT.send_message(message.chat.id, a)
            else:
                name = acc.replace("http://steamcommunity.com/profiles/", "")
                a = parse(getid(name))
                if a == False:
                    BOT.send_message(message.chat.id, "Такого аккаунта нет на дотабаффе")
                else:
                    BOT.send_message(message.chat.id, a)
        elif acc.lower()[1] in "abcdefghijklmnopqrstuvwxyz1234567890":
            name = acc
            ans = parse(getid(name))
            if ans != False:
                BOT.send_message(message.chat.id, ans)
            else:
                BOT.send_message(message.chat.id, "Такого аккаунта нет")
        else:
            BOT.send_message(message.chat.id, "Такого аккаунта нет")
    else:
        BOT.send_message(message.chat.id, "Чтобы чекнуть пиши /check id, например /check xui")
@BOT.message_handler(commands = ["start"])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_checkprofile = telebot.types.KeyboardButton("Чекнуть профиль")
    item_checkmom = telebot.types.KeyboardButton("Чекнуть мать")
    item_myprofile = telebot.types.KeyboardButton("Мой Профиль")
    item_meta = telebot.types.KeyboardButton("Чекнуть Мету")
    markup.add(item_checkprofile, item_checkmom, item_myprofile,item_meta)
    BOT.send_sticker(message.chat.id, "CAACAgIAAxkBAAELprZiT8r9EYQUoVdoFkOEmjYn-M83sAACGwADLfpWFLGyFHWID4PvIwQ", reply_markup= markup)


@BOT.message_handler(commands = ["Back", "back"])
def back(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_checkprofile = telebot.types.KeyboardButton("Чекнуть профиль")
    item_checkmom = telebot.types.KeyboardButton("Чекнуть мать")
    item_myprofile = telebot.types.KeyboardButton("Мой Профиль")
    item_meta = telebot.types.KeyboardButton("Чекнуть Мету")
    markup.add(item_checkprofile, item_checkmom, item_myprofile, item_meta)
    BOT.send_message(message.chat.id, "Назад", reply_markup=markup)


@BOT.message_handler(commands = ["Mid", "Carry", "Hard", "SoftSup", "HardSup", "Average"])
def bot_message(message):
    tran = ["/Average", "/Carry", "/Mid", "/Hard", "/SoftSup", "/HardSup"]
    print(tran)
    x = get_meta(tran.index(message.text))
    if x == False:
        BOT.send_message(message.chat.id, "Ошибочка")
    else:
        BOT.send_message(message.chat.id, x)


@BOT.message_handler(content_types=["text"])
def bot_message(message):
    if message.chat.type =="private":
        if message.text == "Чекнуть профиль":
            BOT.send_message(message.chat.id, "Введи ссылку на steam профиль или ID профиля")
        elif message.text == "Чекнуть Мету":
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            item_carry = telebot.types.KeyboardButton("/Carry")
            item_mid = telebot.types.KeyboardButton("/Mid")
            item_hard = telebot.types.KeyboardButton("/Hard")
            item_softsup = telebot.types.KeyboardButton("/SoftSup")
            item_hardsup = telebot.types.KeyboardButton("/HardSup")
            item_average = telebot.types.KeyboardButton("/Average")
            item_back = telebot.types.KeyboardButton("/Back")
            markup.add(item_carry, item_mid, item_hard, item_softsup, item_hardsup, item_average, item_back)
            BOT.send_message(message.chat.id, "Meta", reply_markup=markup)
        elif message.text == "Чекнуть мать":
            BOT.send_message(message.chat.id, f"Твоя мать {random.choice(mama)}")
        elif message.text.startswith("https://steamcommunity.com/id/"):
            if message.text[-1] == "/":
                name = message.text.replace("https://steamcommunity.com/id/", "")
                name = name[:-1]
                a = parse(getid(name))
                if a == False:
                    BOT.send_message(message.chat.id, "Такого аккаунта нет на дотабаффе")
                else:
                    BOT.send_message(message.chat.id, a)
            else:
                name = message.text.replace("https://steamcommunity.com/id/", "")
                a = parse(getid(name))
                if a == False:
                    BOT.send_message(message.chat.id, "Такого аккаунта нет на дотабаффе")
                else:
                    BOT.send_message(message.chat.id, a)
        elif message.text.startswith("http://steamcommunity.com/profiles/"):
            if message.text[-1] == "/":
                name = message.text.replace("http://steamcommunity.com/profiles/", "")
                name = name[:-1]
                a = parse(getid(name))
                if a == False:
                    BOT.send_message(message.chat.id, "Такого аккаунта нет на дотабаффе")
                else:
                    BOT.send_message(message.chat.id, a)
            else:
                name = message.text.replace("http://steamcommunity.com/profiles/", "")
                a = parse(getid(name))
                if a == False:
                    BOT.send_message(message.chat.id, "Такого аккаунта нет на дотабаффе")
                else:
                    BOT.send_message(message.chat.id, a)
        elif message.text == "Мой Профиль":
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            item_my_profile_check = telebot.types.KeyboardButton("Чекнуть свой профиль")
            item_my_profile_forgot = telebot.types.KeyboardButton("Забыть мой профиль")
            item_sub_on = telebot.types.KeyboardButton("Подписаться на уведомления")
            item_sub_off = telebot.types.KeyboardButton("Отписаться от уведомлений")
            item_back = telebot.types.KeyboardButton("/Back")
            markup.add(item_my_profile_check, item_my_profile_forgot, item_sub_on, item_sub_off, item_back)
            BOT.send_message(message.chat.id, "Мой Профиль", reply_markup=markup)

        elif message.text == "Чекнуть свой профиль":
            prof = myprofile(user_id=message.from_user.id)
            if prof is not None:
                BOT.send_message(message.chat.id, parse(getid(prof[0])))
            else:
                BOT.send_message(message.chat.id, "Введи /reg ссылка/id_профиля")

        elif message.text == "Забыть мой профиль":
            if checkreg(message.from_user.id) == False:
                del_user(message.from_user.id)
                BOT.send_message(message.chat.id, "Ваш профиль удалён из базы данных")
            else:
                BOT.send_message(message.chat.id, "За вами не закреплено аккаунта")

        elif message.text == "Подписаться на уведомления":
            edit_sub(True, message.from_user.id)
            BOT.send_message(message.chat.id, "Вы подписались на уведомления")
        elif message.text == "Отписаться от уведомлений":
            edit_sub(False, message.from_user.id)
            BOT.send_message(message.chat.id, "Вы отписались от уведомлений")
        elif message.text.lower()[1] in "abcdefghijklmnopqrstuvwxyz1234567890":
            name = message.text
            ans = parse(getid(name))
            if ans != False:
                BOT.send_message(message.chat.id, ans)
        elif message.text == "а боты умеют проходить саманту?":
            BOT.send_message(message.chat.id, "Да, в отличии от некоторых людей")

t1 = threading.Thread(target=startbot)
t2 = threading.Thread(target=runScheluders)
t3 = threading.Thread(target=ScheludeDay)
t1.start()
t2.start()
t3.start()
while True:
        schedule.run_pending()
        time.sleep(1)




