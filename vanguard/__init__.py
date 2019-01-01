from flask import Flask, render_template
import os
import jinja2

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_PASSWORD_SALT'] = 'my_precious_two'



'''
In addition to the standard package loader, there is also a choice of loading from the root directory located in documentor
'''
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
ROOT_FOLDER = os.path.join(THIS_FOLDER, 'calc')
extended_loader = jinja2.ChoiceLoader([app.jinja_loader, jinja2.FileSystemLoader(ROOT_FOLDER)])
app.jinja_loader = extended_loader


from vanguard import views
