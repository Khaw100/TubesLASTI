from flask import Flask, make_response, jsonify, request, render_template, redirect
import json
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
# import jwt
# import datetime
# from functools import wraps


app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'lasti'
app.config['SECRET_KEY'] = 'supersecretkey'

mysql = MySQL(app)


@app.route("/t", methods=["GET","POST"])
def index():
    return render_template("tutor.html")


@app.route("/", methods=["GET","POST"])
def upload():
    cur = mysql.connection.cursor()
    if request.method == "POST":
        cur.execute('SELECT * FROM sub_modul')

        # Determine sub_modul_id
        data = cur.fetchall()
        if len(data) == 0:
            submodul_id = 0
        else:
            submodul_id = len(data)

        modul = request.values.get("modul")
        submodul = request.values.get("sub-modul")
        
        cur.execute(f'SELECT id_modul FROM modul WHERE nama_modul = "{modul}"')
        data_id = cur.fetchall()
        print(data_id)
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaa")
        modul_id = 0
        link = request.values.get("link-video")
        materi = request.values.get("materi")
        query = f"INSERT INTO sub_modul VALUES ({submodul_id},'{submodul}','{modul_id}', '{link}', '{materi}')"
        cur.execute(query)
    mysql.connection.commit()

    return render_template('upload.html')


# print("AAAAAAAAAAA")


    # cur = mysql.connection.cursor()
    # cur.execute('SELECT * FROM sub_modul')

    # # Determine sub_modul_id
    # data = cur.fetchall()
    # if len(data) == 0:
    #     submodul_id = 0
    # else:
    #     submodul_id = len(data)
    # cur.execute(f'SELECT id_modul FROM modul WHERE modul = "{modul}"')
    # data_id = cur.fetchall()
    # modul_id = data_id[0]
    # link = request.values.get("link-video")
    # materi = request.values.get("materi")
    # query = f"INSERT INTO sub_modul VALUES ({submodul_id},'{submodul}','{modul_id}', '{link}', '{materi}')"
    # cur.execute(query)
    # mysql.connection.commit()