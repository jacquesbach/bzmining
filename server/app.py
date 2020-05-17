from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flaskext.mysql import MySQL
from datetime import date
import json

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, support_credentials=True)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = ''
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = ''
app.config['MYSQL_DATABASE_HOST'] = ''

mysql.init_app(app)

@app.route('/articles', methods=['GET'])
def get_articles():
    cur = mysql.connect().cursor()

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
    
    if 'dpa' in request.args:
        query_dpa = query + "AND author LIKE 'dpa' "
        query_dpa = query_dpa + ("GROUP BY published_date ORDER BY published_date ASC")
    
    query_all = query + ("GROUP BY published_date ORDER BY published_date ASC")

    cur.execute(query_all, params)
    rows_all = cur.fetchall()
    if 'dpa' in request.args:
        cur.execute(query_dpa, params)
        rows_dpa = cur.fetchall()
    array_of_dicts = []
    if 'dpa' in request.args:
        for i, j in zip(rows_all, rows_dpa):
            dictionary = {
                'date' : str(i[1]),
                'countall' : str(i[0]),
                'countdpa' : str(j[0]) }
            array_of_dicts.append(dictionary)
        return jsonify(array_of_dicts)
    else:
        for row in rows_all:
            dictionary = {
                'date' : str(row[1]),
                'count' : row[0] }
            array_of_dicts.append(dictionary)
        return jsonify(array_of_dicts)

@app.route('/articles/weekday/hour', methods=['GET'])
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

@app.route('/articles/author/count', methods=['GET'])
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

@app.route('/articles/author/length', methods=['GET'])
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

@app.route('/articles/category/premium', methods=['GET'])
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

@app.route('/articles/category/length', methods=['GET'])
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

@app.route('/articles/category/comments', methods=['GET'])
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

@app.route('/articles/hour/length', methods=['GET'])
def get_hour_length():
    cur = mysql.connect().cursor()
    query = "SELECT published_weekday AS weekday, HOUR(published_time) AS time, AVG(length) AS avglength \
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
            'length' : str(row[2]) }
        array_of_dicts.append(dictionary)
    return jsonify(array_of_dicts)

@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

if __name__ == '__main__':
    app.run()