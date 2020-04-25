__author__ = 'Chenge'

from flask import Blueprint,render_template,request,jsonify,session,redirect
from mysqlInfo import sendemail

Main = Blueprint('Main',__name__)

from mysqlInfo.updateemail import Email
Useremail = Email()

from .views import *