from flask import Flask, render_template,url_for, redirect, request, session
import sqlite3
from functools import wraps


def login_witch_check():
    db = sqlite3.connect('my_database.db')
    c = db.cursor()
    username = request.form['username']
    password = request.form['password']
    c.execute('SELECT * FROM Users WHERE username = ? AND password = ?', (username, password ))
    account = c.fetchone()
    if account:
        session['username'] = username
        msg = None
        return msg
    else:
        return 'Неверное имя пользователя / пароль!'
    
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('home_page'))  # Перенаправление на страницу входа
        return f(*args, **kwargs)
    return decorated_function
    

def all_news():
    db = sqlite3.connect('my_database.db')
    c = db.cursor()
    c.execute('SELECT * FROM News ORDER BY id DESC')
    news = c.fetchall()
    db.commit()
    return news

def del_fav(news_id):
    db = sqlite3.connect('my_database.db')
    c = db.cursor()
    username = session['username']
    c.execute('SELECT * FROM Users WHERE username = ? ', (username, ))
    account = c.fetchone()[0]
    c.execute("INSERT INTO Favorites(user_id, news_id)  VALUES (?,?)",(account, news_id))
    c.execute('DELETE FROM Favorites WHERE user_id = ? AND news_id = ? ', (account, news_id))
    db.commit()

def add_fav(news_id):
    db = sqlite3.connect('my_database.db')
    c = db.cursor()
    username = session['username']
    c.execute('SELECT * FROM Users WHERE username = ? ', (username, ))
    user_id = c.fetchone()[0]
    c.execute("INSERT INTO Favorites(user_id, news_id)  VALUES (?,?)",(user_id, news_id))
    db.commit()
    db.close()

def check_fav(news_id,username):
    db = sqlite3.connect('my_database.db')
    c = db.cursor()
    c.execute('SELECT id FROM Users WHERE username = ? ', (username, ))
    user_id = c.fetchone()[0]
    c.execute('SELECT * FROM Favorites WHERE user_id = ? AND news_id = ?', (user_id, news_id,))
    fav = c.fetchone()
    db.commit()
    if not fav:
        fav = 0
    else:
        fav = 1
    return fav
    
def show_fav(username):
    db = sqlite3.connect('my_database.db')
    c = db.cursor()
    c.execute('SELECT news_id FROM Favorites WHERE user_id = ? ', (get_user_id(username),))
    news_ids = c.fetchall()
    fav_news = []
    for news_id in news_ids:
        c.execute('SELECT * FROM News WHERE id = ?', news_id)
        fav_news.append(c.fetchone())
    db.commit()
    return fav_news

def get_user_id(username):
    db = sqlite3.connect('my_database.db')
    c = db.cursor()
    c.execute('SELECT id FROM Users WHERE username = ? ', (username, ))
    user_id = c.fetchone()[0]
    db.commit()
    return user_id

def one_news(news_id):
    db = sqlite3.connect('my_database.db')
    c = db.cursor()
    c.execute('SELECT * FROM News WHERE id = ?', (news_id,))
    news = c.fetchone()
    db.commit()
    return news

def categor_news(news):
    catego = news
    categor = catego.split(',')
    return categor

def up_rait(news_id,user_id):
    flag = 1
    db = sqlite3.connect('my_database.db')
    c = db.cursor()
    c.execute("INSERT INTO Rait(user_id, news_id,raiting)  VALUES (?,?,?)",(user_id, news_id,flag))
    c.execute('SELECT raiting FROM News WHERE id = ?', (news_id,))
    rait = c.fetchone()[0]
    rait += flag
    c.execute("UPDATE News SET raiting = ? WHERE id = ?", (rait, news_id))
    db.commit()


def down_rait(news_id, user_id):
    flag = -1
    db = sqlite3.connect('my_database.db')
    c = db.cursor()
    c.execute("INSERT INTO Rait(user_id, news_id,raiting)  VALUES (?,?,?)",(user_id, news_id,flag))
    c.execute('SELECT raiting FROM News WHERE id = ?', (news_id,))
    rait = c.fetchone()[0]
    rait += flag
    c.execute("UPDATE News SET raiting = ? WHERE id = ?", (rait, news_id))
    db.commit()


def check_rait(news_id, user_id):
    db = sqlite3.connect('my_database.db')
    c = db.cursor()
    c.execute('SELECT raiting FROM Rait WHERE news_id = ? AND user_id = ?', (news_id, user_id))
    rait = c.fetchone()
    db.commit()
    if rait is None:
        ok=0
    elif rait[0]==1:
        ok=1
    else:ok = -1
    return ok

def del_rait(news_id,user_id,flag):
    db = sqlite3.connect('my_database.db')
    c = db.cursor()
    c.execute('DELETE FROM Rait WHERE user_id = ? AND news_id = ? ', (user_id, news_id))
    c.execute('SELECT raiting FROM News WHERE id = ?', (news_id,))
    rait = c.fetchone()[0]
    rait += flag
    c.execute("UPDATE News SET raiting = ? WHERE id = ?", (rait, news_id))
    db.commit()


def add_news_comment(comm,nowtime,user_id,news_id):
    db = sqlite3.connect('my_database.db')
    c = db.cursor()
    c.execute("INSERT INTO Comm(user_id, news_id, date, comm)  VALUES (?,?,?,?)",(user_id, news_id, nowtime, comm))
    c.execute('SELECT comm FROM News WHERE id = ?', (news_id,))
    ccomm = c.fetchone()[0]
    ccomm += 1
    c.execute("UPDATE News SET comm = ? WHERE id = ?", (ccomm, news_id))
    db.commit()

def get_comm_users_news(news_id):
    db = sqlite3.connect('my_database.db')
    c = db.cursor()
    c.execute('SELECT * FROM Comm WHERE news_id = ?', (news_id,))
    info_comm_users = c.fetchall()
    db.commit()
    return info_comm_users

def get_user_self(username):
    db = sqlite3.connect('my_database.db')
    c = db.cursor()
    c.execute('SELECT * FROM Users WHERE username = ?', (username,))
    user = c.fetchone()
    db.commit()
    return user

def get_users_comm(news_id):
    db = sqlite3.connect('my_database.db')
    c = db.cursor()
    c.execute('''SELECT Users.username,img
    FROM Comm 
    INNER JOIN Users ON Comm.user_id = Users.id
    WHERE Comm.news_id = ?''', (news_id,))
    comm_users = c.fetchall()
    db.commit()
    return comm_users

def comm_profile(user_id):
    db = sqlite3.connect('my_database.db')
    c = db.cursor()
    c.execute('SELECT * FROM Comm WHERE user_id = ?', (user_id, ))
    pcomm = c.fetchall()
    db.commit()
    return pcomm

def count_view(news_id):
    db = sqlite3.connect('my_database.db')
    c = db.cursor()
    c.execute('SELECT view FROM News WHERE id = ?', (news_id, ))
    count = c.fetchone()[0]
    count +=1
    c.execute('UPDATE News SET view = ? WHERE id=?', (count,news_id))
    db.commit()


def top_news():
    db = sqlite3.connect('my_database.db')
    c = db.cursor()
    c.execute('SELECT * FROM News ORDER BY view DESC LIMIT 5')
    topf = c.fetchall()
    db.commit()
    return topf


def first_sentence(text):
    sentences = text.split('.')
    return sentences[0]

def get_terms():
    db = sqlite3.connect('my_database.db')
    c = db.cursor()
    c.execute('SELECT * FROM Term')
    terms = c.fetchall()
    db.commit()
    # Создаем новый список, где для каждого термина мы сохраняем только первое предложение в тексте
    abbreviated_terms = [(term[0], term[1], first_sentence(term[2])) for term in terms]
    return abbreviated_terms

def get_term(id):
    db = sqlite3.connect('my_database.db')
    c = db.cursor()
    c.execute('SELECT * FROM Term WHERE id=?', (id, ))
    term = c.fetchone()
    db.commit()
    return term