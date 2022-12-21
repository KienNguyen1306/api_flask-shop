from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail





app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///QLDL_DATA_SHOP.db"
app.secret_key = 'sdfsdfdsfsfcxvxcvsnsfsda21654dasdvcvbvbcvfefdsf'
app.config['SIZE_PRODUCT']=100
# initialize the app with the extension
db = SQLAlchemy(app)


mail = Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='kienndk09@gmail.com'
app.config['MAIL_PASSWORD']='adpoiaccuwsamfjv'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail = Mail(app)



db.init_app(app)