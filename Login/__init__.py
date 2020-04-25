__author__ = 'Chenge'
from flask import Blueprint,render_template,request,jsonify,session,redirect
from mysqlInfo import loginsql
import datetime
from mysqlInfo import sendemail
import base64

Login = Blueprint('Login',__name__)

Userlogin = loginsql.Login()
Userregister = loginsql.Register()
Userreset = loginsql.Reset()

from .views import *

