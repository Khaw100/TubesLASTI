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

@app.route("/tutor", methods=["GET","POST"])
def index():
    return render_template("tutor.html")

# http://127.0.0.1:5000/edit/tutor/0/modul/0/0
@app.route("/tutor/edit/<kelas>/modul/<modul>/<submodul>", methods=["GET","POST"])
def tutor(kelas,modul,submodul):
    cur = mysql.connection.cursor()
    if request.method =="POST":
        linkYTB = request.form['link-youtube']
        linkYTB = linkYTB.replace('watch?v=',"embed/")
        materi = request.form['materi']
        namaSubModul = 'Persiapan Belajar'
        if materi == '' and linkYTB != '':
            query = f"update sub_modul set video ='{linkYTB}' where id_sub_modul = {submodul} and id_modul = {modul}"
            print(query)
            cur.execute(query)
            mysql.connection.commit()
        elif linkYTB == '' and materi != '': 
            query = f"update sub_modul set materi ='{materi}' where id_sub_modul = {submodul} and id_modul = {modul}"
            cur.execute(query)
            mysql.connection.commit()
        elif materi != '' and  linkYTB != '':
            query = f"update sub_modul set video ='{linkYTB}', materi = '{materi}' where id_sub_modul = {submodul} and id_modul = {modul}"
            cur.execute(query)
            mysql.connection.commit()
        print('######### TEST ###########')
    print(kelas,modul,submodul)
    return render_template("tutor.html")
# http://127.0.0.1:5000/tutor/addSub/0/modul/0/0
@app.route("/tutor/addSub/<kelas>/modul/<modul>/<submodul>", methods=["GET","POST"])
def addSub(kelas,modul,submodul):
    cur = mysql.connection.cursor()
    if request.method =="POST":
        linkYTB = request.form['link-youtube']
        linkYTB = linkYTB.replace('watch?v=',"embed/")
        materi = request.form['materi']
        print(linkYTB,materi)
        namaSubModul = 'Persiapan Belajar'
        query = f"INSERT INTO sub_modul VALUES ({submodul},'{namaSubModul}',{modul}, '{linkYTB}', '{materi}')"
        print(query)
        cur.execute(query)
        mysql.connection.commit()
        print('######### TEST ###########')
    print(kelas,modul,submodul)
    return render_template("tutor.html")

# http://127.0.0.1:5000/pengguna/0/modul/0/0
@app.route("/pengguna/<kelas>/modul/<modul>/<submodul>", methods=["GET","POST"])
def pengguna(kelas,modul,submodul):
    cur = mysql.connection.cursor()
    query = f'select video,materi from sub_modul where id_sub_modul = {submodul} and id_modul = {modul}'
    cur.execute(query)
    print(query)
    data = cur.fetchall()
    if len(data) == 0:
        data = (("","Materi belum dibuat"),)
    print(f'data: {data}')
    # print(data[0][0])
    return render_template('pengguna.html',data=data)


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