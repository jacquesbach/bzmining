from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin
from flaskext.mysql import MySQL
from app import app
from datetime import date
import datetime
import json
import os

mysql = MySQL()

loginpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'mysqllogin.txt')
credentials = {}
with open(loginpath, 'r') as f:
    for line in f:
        host, db, user, pwd = line.strip().split(';')
        credentials = host, db, user, pwd

# MySQL configurations
app.config['MYSQL_DATABASE_HOST'] = credentials[0]
app.config['MYSQL_DATABASE_DB'] = credentials[1]
app.config['MYSQL_DATABASE_USER'] = credentials[2]
app.config['MYSQL_DATABASE_PASSWORD'] = credentials[3]

mysql.init_app(app)

@app.route('/api')
def index():
    user = {'username': 'mein Freund'}
    now = datetime.datetime.now()
    if now.hour >= 0 and now.hour <= 6:
        greeting = "Gute Nacht"
    elif now.hour >= 6 and now.hour <= 12:
        greeting = "Guten Morgen"
    elif now.hour >= 12 and now.hour <= 18:
        greeting = "Schönen Nachmittag"
    elif now.hour >= 18 and now.hour <= 24:
        greeting = "Guten Abend"
    return render_template('index.html', title='Home', user=user, greeting=greeting)

@app.route('/api/articles', methods=['GET'])
def get_articles():
    query = "SELECT COUNT(*) as count, published_date as date from articles "

    if 's' in request.args:
        search_term = str(request.args['s'])
    if 'author' in request.args:
        author_term = str(request.args['author'])
    if 'title' in request.args:
        title_term = str(request.args['title'])

    if 's' in request.args and 'author' in request.args and 'title' in request.args:
        query = query + "WHERE content LIKE %s AND author LIKE %s AND title LIKE %s AND published_date >= '2020-02-08' AND published_date IS NOT NULL "
        params = ("%{}%".format(search_term), "%{}%".format(author_term), "%{}%".format(title_term))
    elif 's' not in request.args and 'author' in request.args and 'title' in request.args:
        query = query + "WHERE author LIKE %s AND title LIKE %s AND published_date >= '2020-02-08' AND published_date IS NOT NULL "
        params = ("%{}%".format(author_term), "%{}%".format(title_term))
    elif 'author' not in request.args and 's' in request.args and 'title' in request.args:
        query = query + "WHERE content LIKE %s AND title LIKE %s AND published_date >= '2020-02-08' AND published_date IS NOT NULL "
        params = ("%{}%".format(search_term), "%{}%".format(title_term))
    elif 'title' not in request.args and 's' in request.args and 'author' in request.args:
        query = query + "WHERE content LIKE %s AND author LIKE %s AND published_date >= '2020-02-08' AND published_date IS NOT NULL "
        params = ("%{}%".format(search_term), "%{}%".format(author_term))
    elif 's' not in request.args and 'author' not in request.args and 'title' in request.args:
        query = query + "WHERE title LIKE %s AND published_date >= '2020-02-08' AND published_date IS NOT NULL "
        params = ("%{}%".format(title_term))
    elif 'author' not in request.args and 'title' not in request.args and 's' in request.args:
        query = query + "WHERE content LIKE %s AND published_date >= '2020-02-08' AND published_date IS NOT NULL "
        params = ("%{}%".format(search_term))
    elif 'title' not in request.args and 's' not in request.args and 'author' in request.args:
        query = query + "WHERE author LIKE %s AND published_date >= '2020-02-08' AND published_date IS NOT NULL "
        params = ("%{}%".format(author_term))
    else:
        query = query + "WHERE published_date >= '2020-02-08' AND published_date IS NOT NULL "
        params = ()
    
    query_dpa = query + "AND author = 'dpa' "
    query_dpa = query_dpa + "GROUP BY published_date ORDER BY published_date ASC"
    
    query_all = query + "GROUP BY published_date ORDER BY published_date ASC"

    cur1 = mysql.connect().cursor()
    cur1.execute(query_all, params)
    rows_all = cur1.fetchall()
    cur1.close()
    array_of_all_dicts = []
    for row in rows_all:
        dictionary = {
            'date' : str(row[1]),
            'count' : row[0],
            'countdpa' : 0 }
        array_of_all_dicts.append(dictionary)
    cur2 = mysql.connect().cursor()
    cur2.execute(query_dpa, params)
    rows_dpa = cur2.fetchall()
    cur2.close()
    array_of_dpa_dicts = []
    for row in rows_dpa:
        dictionary = {
            'date' : str(row[1]),
            'countdpa' : row[0] }
        array_of_dpa_dicts.append(dictionary)
    for e,v in zip(array_of_all_dicts,array_of_dpa_dicts):
        e.update(v)
    return jsonify(array_of_all_dicts)

@app.route('/api/articles/weekday/hour', methods=['GET'])
def get_weekday_hour():
    cur = mysql.connect().cursor()
    query = "SELECT published_weekday AS weekday, HOUR(published_time) AS time, COUNT(*) AS count \
        FROM articles \
        WHERE published_weekday IS NOT NULL \
        AND published_time IS NOT NULL \
        GROUP BY published_weekday, HOUR(published_time) \
        ORDER BY FIELD(published_weekday, 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag') ASC, HOUR(published_time) ASC"
    cur.execute(query)
    rows = cur.fetchall()
    array_of_dicts = []
    for row in rows:
        dictionary = {
            'weekday' : str(row[0]),
            'hour' : row[1],
            'count' : row[2] }
        array_of_dicts.append(dictionary)
    return jsonify(array_of_dicts)

@app.route('/api/articles/author/count', methods=['GET'])
def get_author_count():
    cur = mysql.connect().cursor()
    query = "SELECT author AS author, COUNT(*) AS count \
        FROM articles \
        WHERE published_date >= '2020-02-08' \
        AND NOT author='dpa' \
        AND NOT author='BZ-Redaktion' \
        AND NOT author='afp' \
        AND NOT author='sda' \
        AND NOT author='kna' \
        AND NOT author='epd' \
        AND NOT author='AFP' \
        AND NOT author='' \
        AND NOT author='SP-X' \
        AND NOT author='sth' \
        AND NOT author='tmn' \
        GROUP BY author \
        ORDER BY COUNT(*) DESC \
        LIMIT 100"
    cur.execute(query)
    rows = cur.fetchall()
    array_of_dicts = []
    for row in rows:
        dictionary = {
            'author' : str(row[0]),
            'count' : row[1] }
        array_of_dicts.append(dictionary)
    return jsonify(array_of_dicts)

@app.route('/api/articles/author/length', methods=['GET'])
def get_author_length():
    cur = mysql.connect().cursor()
    query = "SELECT author AS author, AVG(length) AS laenge \
        FROM articles \
        WHERE length > 0 \
        AND premium='0' \
        AND author IS NOT NULL \
        GROUP BY author \
        ORDER BY laenge DESC \
        LIMIT 100"
    cur.execute(query)
    rows = cur.fetchall()
    array_of_dicts = []
    for row in rows:
        dictionary = {
            'author' : str(row[0]),
            'length' : str(row[1]) }
        array_of_dicts.append(dictionary)
    return jsonify(array_of_dicts)

@app.route('/api/articles/category/premium', methods=['GET'])
def get_category_premium():
    cur = mysql.connect().cursor()
    query = "SELECT submenu_category AS category, AVG(premium) AS plus \
        FROM articles \
        WHERE published_date >= '2020-02-08' \
        AND NOT submenu_category='Sonderthemen' \
        GROUP BY submenu_category \
        ORDER BY AVG(premium) DESC"
    cur.execute(query)
    rows = cur.fetchall()
    array_of_dicts = []
    for row in rows:
        dictionary = {
            'category' : str(row[0]),
            'premium' : str(row[1]) }
        array_of_dicts.append(dictionary)
    return jsonify(array_of_dicts)

@app.route('/api/articles/category/length', methods=['GET'])
def get_category_length():
    cur = mysql.connect().cursor()
    query = "SELECT submenu_category AS category, AVG(length) AS avglength \
        FROM articles \
        WHERE published_date >= '2020-02-08' \
        AND submenu_category IS NOT NULL \
        AND length IS NOT NULL \
        AND NOT submenu_category='Sonderthemen' \
        AND NOT submenu_category='Über uns' \
        AND premium='0' \
        GROUP BY submenu_category \
        ORDER BY avglength DESC"
    cur.execute(query)
    rows = cur.fetchall()
    array_of_dicts = []
    for row in rows:
        dictionary = {
            'category' : str(row[0]),
            'length' : str(row[1]) }
        array_of_dicts.append(dictionary)
    return jsonify(array_of_dicts)

@app.route('/api/articles/category/comments', methods=['GET'])
def get_category_comments():
    cur = mysql.connect().cursor()
    query = "SELECT submenu_category AS category, AVG(comments) AS avgcomments \
        FROM articles \
        WHERE published_date >= '2020-02-08' \
        AND premium='0' \
        AND submenu_category IS NOT NULL \
        AND NOT submenu_category='Sonderthemen' \
        AND comments IS NOT NULL \
        GROUP BY submenu_category \
        ORDER BY avgcomments DESC"
    cur.execute(query)
    rows = cur.fetchall()
    array_of_dicts = []
    for row in rows:
        dictionary = {
            'category' : str(row[0]),
            'comments' : str(row[1]) }
        array_of_dicts.append(dictionary)
    return jsonify(array_of_dicts)

@app.route('/api/articles/hour/length', methods=['GET'])
def get_hour_length():
    cur = mysql.connect().cursor()
    query = "SELECT published_weekday AS weekday, HOUR(published_time) AS time, count(*) as count, AVG(length) AS avglength \
        FROM articles \
        WHERE published_weekday IS NOT NULL \
        AND published_time IS NOT NULL \
        GROUP BY published_weekday, HOUR(published_time) \
        ORDER BY FIELD(published_weekday, 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag') ASC, HOUR(published_time) ASC"
    cur.execute(query)
    rows = cur.fetchall()
    array_of_dicts = []
    for row in rows:
        dictionary = {
            'weekday' : str(row[0]),
            'hour' : row[1],
            'count' : row[2],
            'length' : str(row[3]) }
        array_of_dicts.append(dictionary)
    return jsonify(array_of_dicts)

@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')