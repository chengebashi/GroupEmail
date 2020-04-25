__author__ = 'Chenge'
from flask import Flask,session,render_template
from Login import Login
from Main import Main

app = Flask(__name__)

app.secret_key = b'\xf9\x7f\xc5\xa2c\xd02\xd9\x95E$RM\xf2\xb3}\x18\xc5\xae\x14Ot#Q'



app.register_blueprint(Login,url_prefix='/admin/')
app.register_blueprint(Main)




@app.errorhandler(404)
def pagenotfound(e):
    return render_template('Login/404.html')


if __name__ == '__main__':
    app.run(port=80,debug=True)
