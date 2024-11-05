from flask import Flask, render_template,url_for, redirect, request, session
from werkzeug.utils import secure_filename
import os
import sqlite3
import funcs
from werkzeug.utils import secure_filename
from nowtime import get_now_time
from funcs import all_news, login_required, del_fav,add_fav,check_fav, one_news, categor_news,login_witch_check, show_fav, up_rait, down_rait, check_rait, get_user_id, del_rait, add_news_comment, get_comm_users_news, get_user_self, get_users_comm, comm_profile, count_view, top_news, get_terms, get_term


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

UPLOAD_FOLDER = "user_avatar/"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER





@app.route("/")
@app.route("/home")
def home_page():
    username = session.get('username', 'Войти')
    msg = request.args.get('msg')
    return render_template('index.html', username=username, msg=msg, news=all_news(), top = top_news())



@app.route("/login", methods=['POST'])
def login():
    return redirect(url_for("home_page", msg = login_witch_check()))

@app.route("/register", methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    rep_password = request.form['rep_password']
    db = sqlite3.connect('my_database.db')
    c = db.cursor()
    c.execute('SELECT * FROM Users WHERE username = ? ', (username, ))
    account = c.fetchone()
    if account:
        msg = 'Учетная запись уже существует!'
        return redirect(url_for("home_page", msg = msg))
    else:
        c.execute('INSERT INTO Users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
        db.commit()
        msg = 'Вы успешно зарегистрировались!'
        return redirect(url_for("home_page", msg = msg))


@app.route("/logout")
def logout():
   session.clear()
   return redirect(url_for('home_page'))

# for news


def alln():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM News")
    anews = cursor.fetchall()
    return anews


@app.route("/news/<int:news_id>")
def news_page(news_id):
    count_view(news_id)
    username = session.get('username', 'Войти')
    if not session:
        return render_template('news.html', username=username, news=one_news(news_id), categor=categor_news(one_news(news_id)[9]), comm_users=get_comm_users_news(news_id), users_comm_i=get_users_comm(news_id))
    else: 
        username = session['username']
        user_id = get_user_id(username)
        print(get_users_comm(news_id))
        return render_template('news.html', username=username, news=one_news(news_id), categor=categor_news(one_news(news_id)[9]), fav=check_fav(news_id,username), rait=check_rait(news_id, user_id), comm_users=get_comm_users_news(news_id),users_comm_i=get_users_comm(news_id))

@app.route("/add_to_favorites/<int:news_id>", methods=['GET'])
def add_to_favorites(news_id):
    add_fav(news_id)
    return redirect(url_for("news_page",news_id=news_id))

@app.route("/del_to_favorites/<int:news_id>", methods=['GET'])
def del_to_favorites(news_id):
    del_fav(news_id)
    return redirect(url_for("news_page", news_id=news_id))

@app.route("/del_to_favorites_to_profile/<int:news_id>", methods=['GET'])
def del_to_favorites_to_profile(news_id):
    del_fav(news_id)
    return redirect(url_for("profile_page", news_id=news_id))


@app.route("/rait-up/<int:news_id>", methods=['GET'])
def rait_up(news_id):
    username = session['username']
    user_id = get_user_id(username)
    up_rait(news_id, user_id)
    return redirect(url_for("news_page", news_id=news_id))
# 
@app.route("/rait-down/<int:news_id>", methods=['GET'])
def rait_down(news_id):
    username = session['username']
    user_id = get_user_id(username)
    down_rait(news_id, user_id)
    return redirect(url_for("news_page", news_id=news_id))
# 
@app.route("/rait-delp//<int:news_id>", methods=['GET'])
def rait_delp(news_id):
    user_id=get_user_id(session['username'])
    del_rait(news_id,user_id,1)
    return redirect(url_for("news_page", news_id=news_id))

@app.route("/rait-delm//<int:news_id>", methods=['GET'])
def rait_delm(news_id):
    user_id=get_user_id(session['username'])
    del_rait(news_id,user_id,-1)
    return redirect(url_for("news_page", news_id=news_id))

@app.route("/reprait-delm//<int:news_id>", methods=['GET'])
def reprait_delm(news_id):
    user_id=get_user_id(session['username'])
    del_rait(news_id,user_id,-1)
    down_rait(news_id, user_id)
    return redirect(url_for("news_page", news_id=news_id))

@app.route("/reprait-delp//<int:news_id>", methods=['GET'])
def reprait_delp(news_id):
    user_id=get_user_id(session['username'])
    del_rait(news_id,user_id,1)
    up_rait(news_id, user_id)
    return redirect(url_for("news_page", news_id=news_id))

@app.route("/add-news-comm/<int:news_id>", methods=['POST'])
def add_news_comm(news_id):
    comm = request.form['comm']
    nowtime = get_now_time()
    user_id=get_user_id(session['username'])
    add_news_comment(comm,nowtime,user_id,news_id)
    return redirect(url_for('news_page', news_id=news_id))



@app.route("/recommendations")
def rec_page():
   username = session.get('username', 'Войти')
   return render_template('rec.html', username=username)


@app.route("/dictionary")
def dictionary_page():
   username = session.get('username', 'Войти')
   return render_template('dict.html', username=username, terms=get_terms())


@app.route("/termin/<int:tid>")
def termin_page(tid):
    username = session.get('username', 'Войти')
    print(get_term(tid))
    term = get_term(tid)
    fletter = term[1][0]
    print(fletter)
    return render_template('termin.html', username=username, term=term, fletter=fletter)



# for profile




@app.route("/profile")
@login_required
def profile_page():
    username = session.get('username')
    print(comm_profile(get_user_id(username)))
    return render_template('profile.html', username=username, fav_news=show_fav(username), user=get_user_self(username), pcomm = comm_profile(get_user_id(username)))
    

if __name__ == '__main__':
  app.run(debug=True)