from flask import Flask, redirect, url_for, render_template, make_response, request, session
import hashlib
from datetime import datetime
import json
from database import connectToDatabase
import sys

import random

import socket

app = Flask(__name__, static_folder="public", template_folder='templates')

currentSessions = {}

def is_connected(request):
    token = request.cookies.get('session')
    conn, cur = connectToDatabase()
    select_query = 'SELECT username, coins, hasFreeCoin FROM web_users WHERE currentToken=%s'
    cur.execute(select_query, (token,))
    res = cur.fetchall()
    cur.close()
    if len(res) > 0:
        return {
            "username": res[0][0],
            "coins": res[0][1],
            "hasFreeCoin": res[0][2]
        }
    else:
        return False

def connect_user(username, password):
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    conn, cur = connectToDatabase()
    select_query = 'SELECT username FROM web_users WHERE username=%s and password=%s'
    cur.execute(select_query, (username, password))
    res = cur.fetchall()
    cur.close()
    if len(res) > 0:
        name = res[0]
        token = hashlib.sha256((str(datetime.now().timestamp()) + username).encode('utf-8')).hexdigest()
        conn, cur = connectToDatabase()
        query = 'UPDATE web_users SET currentToken=%s where username=%s'
        cur.execute(query, (token, name))
        conn.commit()
        cur.close()
        return token
    else:
        return False

def change_coins(username, coins):
    if coins >= 0:
        conn, cur = connectToDatabase()
        query = 'UPDATE web_users SET coins=%s where username=%s'
        cur.execute(query, (coins, username))
        conn.commit()
        cur.close()
        return True
    else:
        return False

def create_account(username, password):
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    conn, cur = connectToDatabase()
    select_query = 'SELECT username FROM web_users WHERE username=%s'
    cur.execute(select_query, (username,))
    res = cur.fetchall()
    cur.close()
    if len(res) > 0:
        return False
    else:
        conn, cur = connectToDatabase()
        query = 'INSERT INTO web_users (username, password, coins, hasFreeCoin) values (%s, %s, 0, false)'
        cur.execute(query, (username, password))
        conn.commit()
        cur.close()
        return True

def create_free_coins_ticket(username):
    conn, cur = connectToDatabase()
    query = 'INSERT INTO freecoins (token, amount) values (%s, 5);'
    token = ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890") for x in range(32))
    cur.execute(query, (token,))
    conn.commit()
    cur.close()
    conn, cur = connectToDatabase()
    query = 'UPDATE web_users SET hasFreeCoin=true where username=%s;'
    cur.execute(query, (username,))
    conn.commit()
    cur.close()
    return token

def verify_voucher(voucher):
    conn, cur = connectToDatabase()
    select_query = 'SELECT amount FROM freecoins WHERE token=%s'
    cur.execute(select_query, (voucher,))
    res = cur.fetchall()
    cur.close()
    if len(res) > 0:
        return res[0][0]
    else:
        return 0


def send_command_to_minecraft(command):
    hote = "localhost"
    port = 15555
    byte_payload = bytes(command, 'utf-8')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hote, port))

    s.send(byte_payload)

    s.close()


@app.route("/register", methods = ['POST','GET'])
def register():
    if request.method == 'GET':
        return render_template('/register.html')
    else:
        user_created = create_account(request.form['username'], request.form['password'])
        
        if user_created:
            return redirect('/login')
        else :
            return render_template("fail.html", message="Impossible de créer un compte : ce compte existe déjà !"), 400


            
            
@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('/login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        token = connect_user(username, password)
        if token:
            resp = make_response(redirect('/'))
            resp.set_cookie('session', token)
            return resp
        else:
            return "Nope", 401

@app.route("/", methods = ['GET'])
def connected():
    user = is_connected(request)
    if user:
        return render_template("main_page.html", user=user)
    else:
        return render_template("main_page.html", user=None)


@app.route("/store", methods = ['GET', 'POST'])
def store():
    user = is_connected(request)
    if user:
        if request.method == 'GET':
            return render_template("store.html", user=user)
        else:
            choice = request.form['choice']
            if choice != "":
                if change_coins(user['username'], user['coins'] - 10):
                    choice = choice.replace("'", "")
                    send_command_to_minecraft("execute at @a positioned ~ ~ ~ run summon " + choice + " ~ ~ ~")
                    return render_template("success.html", achat=choice, user=user)
                else:
                    return render_template("fail.html", message="Vous n'avez pas assez d'argent :(", user=user)
            else:
                render_template("store.html", user=user)

    else:
        return redirect("/login")

@app.route("/claim", methods = ['GET'])
def claim():
    user = is_connected(request)
    if user:
        if user["hasFreeCoin"]:
            return render_template("fail.html", message="Vous avez déjà réclamé l'argent gratuit !", user=user)
        token = create_free_coins_ticket(user['username'])
        return redirect('/freecoins?voucher=' + str(token))
    else:
        return redirect("/login")

@app.route("/freecoins", methods = ['GET'])
def freecoins():
    user = is_connected(request)
    if user:
        amount = verify_voucher(request.args.get('voucher'))
        if amount > 0:
            change_coins(user['username'], user['coins'] + amount)
            return redirect('/')
        else:
            return render_template('fail.html', message="Le coupon n'est pas valide", user=user)
    else:
        return redirect("/login")

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)