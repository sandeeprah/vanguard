from flask import request, render_template, jsonify, abort, make_response
#from flask_httpauth import HTTPBasicAuth
from vanguard import app
from vanguard.calc import views


@app.route('/')
@app.route('/index/')
def index():
    return render_template("index.html")




'''

@app.route('/')
@app.route('/index/')
def index():
    return render_template("index.html")

@app.route('/admin/')
def admin():
    return render_template("admin.html")

@app.route('/login/')
def login():
    return render_template("login.html")

@app.route('/google5ca5209499debead.html')
def google_verify():
    return render_template("google5ca5209499debead.html")

@app.route('/sitemap.xml')
def google_sitemap():
    template = render_template('sitemap.xml')
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'
    return response

@app.route('/robots.txt')
def google_robots():
    template = render_template('robots.txt')
    response = make_response(template)
    response.headers['Content-Type'] = 'text/plain'
    return response

@app.route('/forgot/', methods=['GET'])
def forgot_password():
    return render_template("forgot_password.html")

@app.route('/register/', methods=['GET'])
def register_user():
    return render_template("register.html")

@app.route('/profile/', methods=['GET'])
def profile_user():
    return render_template("profile.html")

@app.route('/indexlogin/', methods=['GET'])
def index_user():
    return render_template("indexlogin.html")
'''
