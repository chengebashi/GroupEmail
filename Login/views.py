__author__ = 'Chenge'
from . import *

@Login.route('login',methods=['GET','POST'])
def login():
    '''用户登陆'''
    if request.method == 'GET':
        username = session.get('username')  #判断用户名seesion是否存在，若存在跳转主页，否则跳转登陆界面
        if username:
            return redirect('/')
        else:
            return render_template('Login/login.html')
    else:
        data = request.get_json()   #获取前端ajax传递过来的数据
        email = data['emailValue']
        password = data['passwordValue']
        #检验密码
        res = Userlogin.checkEmail(email)    #数据库校验邮箱是否存在
        if res != 0:
            return jsonify({'err':'邮箱不存在！'})
        else:
            reg = Userlogin.checkPasswd(email,password)       #数据库校验密码是否正确
            if reg == 1:
                return jsonify({'err':'密码错误!'})
            else:
                info = Userlogin.showAllinfo(email)         #获得该登陆用户的所有基本信息
                session['head'] = '../../'+info[1]
                session['username'] = info[2]
                session['password'] = info[3]
                session['email'] = info[4]
                # session['message'] = D.mainfourmessage()[::-1]
                session['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                return jsonify({'err':0})


@Login.route('/logout',methods=['GET'])
def logout():
    '''用户注销，清空所有session'''
    session.pop('username')
    session.pop('email')
    session.pop('password')
    session.pop('head')
    # session.pop('message')
    #跳转登陆界面
    return redirect('login')

@Login.route('register',methods=['GET','POST'])
def register():
    '''用户注册'''
    if request.method == 'GET':
        username = session.get('username')  #判断用户名seesion是否存在，若存在跳转主页，否则跳转登陆界面
        if username:
            return redirect('/')
        else:
            return render_template('Login/register.html')
    else:
        data = request.get_json()     #获取前端ajax传递过来的数据
        username = data['usernameValue']
        email = data['emailValue']
        password = data['passwordValue']
        res = Userregister.checkEmail(email)    #数据库校验邮箱是否存在
        if res == 1:
            ree = Userregister.checkUname(username) #数据库校验用户名是否存在
            if ree == 0:
                return jsonify({'err':'用户名已存在！'})
            else:
                reg = Userregister.registerUser(username,password,email)        #写入新用户数据
                if reg == 0:
                    return jsonify({'err':0})
                else:
                    return jsonify({'err':'后台错误！'})
        else:
            return jsonify({'err':'邮箱名已存在！'})

@Login.route('/resetpassword',methods=['GET','POST'])
def resetpassword():
    '''找回密码'''
    if request.method == 'GET':
        username = session.get('username')  #判断用户名seesion是否存在，若存在跳转主页，否则跳转登陆界面
        if username:
            return redirect('/')
        else:
            return render_template('Login/resetpassword.html')
    else:
        data = request.get_json() #获取前端ajax传递过来的数据
        username = data['username_value']
        randomNumber = data['randomnumber']
        if randomNumber != session['randomNumber']:      #判断验证码是否一致
            return jsonify({'err':'验证码错误!'})
        else:
            res = Userreset.checkUname(username)   #数据库校验用户名是否存在
        if res == 0:
            return jsonify({'err':'用户名不存在'})
        else:
            reg = Userreset.resetpasswd(username)
            if reg == 0:
                email = Userreset.showemail(username)
                sendemail.email_send('重置密码','初始化密码:123456',[email])    #重置后的密码发送至邮箱
                return jsonify({'err':0})
            else:
                return jsonify({'err':'后台错误'})

@Login.route('/randomNumber',methods=['POST'])
def randomNumber():
    data = request.get_json()     #获取前端ajax传递过来的数据
    nowName = data['nowname']
    now_email = Userreset.showemail(nowName)
    randomNumber = sendemail.randomnumber()  #得到六位随机数
    session['randomNumber'] = str(randomNumber)
    err = sendemail.email_send('验证码','当前的验证码为'+str(randomNumber)+',请不要告诉别人哦！',[now_email]) #发送验证码
    return jsonify({'err':err})

@Login.route('/randomNumber2',methods=['POST'])
def randomNumber2():
    data = request.get_json()
    nowName = data['nowname']
    res = Userreset.checkUname(nowName)
    if res == 0:
        return jsonify({'err':'用户名不存在！'})
    else:
        now_email = Userreset.showemail(nowName)
        randomNumber = sendemail.randomnumber()
        session['randomNumber'] = str(randomNumber)
        err = sendemail.email_send('验证码','当前的验证码为'+str(randomNumber)+',请不要告诉别人哦！',[now_email])   #发送验证码
        return jsonify({'err':err})


@Login.route('/updatepassword',methods=['GET','POST'])
def updatepassword():
    '''更新密码'''
    if request.method=='GET':
        uname = session.get('username')
        if not uname:
            return redirect('login')
        else:
            img = session['head']
            img = img + '?r=' + str(sendemail.randomnumber())
            email = session['email']
            return render_template('Login/updatePassword.html',uname=uname,nowtime=session['time'],img=img)
    else:
        data = request.get_json()    #拿到AJax
        newpass = data['newpass']
        randomNumber = data['randomnumber']
        if randomNumber != session['randomNumber']:
            return jsonify({'err':'验证码错误'})
        else:
            res = Userreset.updatePssword(session['username'],newpass)   #更新数据库用户密码
            if res == 0:
                session['password'] = newpass
                session.pop('randomNumber')
                return jsonify({'err':0})
            else:
                return jsonify({'err':'后台错误!'})


@Login.route('/updatehead',methods=['GET','POST'])
def updatehead():
    '''更新头像'''
    if request.method=='GET':
        uname = session.get('username')
        email = session.get('email')
        imgpath = session.get('head')
        imgpath = imgpath + '?r=' + str(sendemail.randomnumber())  #防止浏览器缓存
        if not uname:
            return redirect('login')
        else:
            img = session['head']
            img = img + '?r=' + str(sendemail.randomnumber())
            return render_template('Login/updatehead.html',uname=uname,email=email,imgpath=imgpath,nowtime=session['time'],img=img)
    else:
        data = request.get_json()
        img = data['img']
        end = img.split(';')[0].split('/')[-1]
        uid = Userreset.showuid(session['username'])
        session['path'] = 'static/assets/headimg'
        os_path = session['path']+'/'+str(uid)+'.'+end
        with open(os_path, 'wb') as f:
            data_img = base64.b64decode(img.split(',')[-1])
            f.write(data_img)
        res = Userreset.updateheadimg(uid,os_path)     #更新数据库用户头像
        if res==0:
            session['head'] = '../../'+os_path       #刷新session
            return jsonify({'err':0})
        else:
            return jsonify({'err':'后台错误!'})

@Login.route('/updateemail',methods=['GET','POST'])
def updateemail():
    '''更新邮箱'''
    if request.method=='GET':
        uname = session.get('username')
        if not uname:
            return redirect('login')
        else:
            img = session['head']
            img = img + '?r=' + str(sendemail.randomnumber())
            email = session['email']
            return render_template('Login/updateemail.html',uname=uname,nowtime=session['time'],img=img,email=email)
    else:
        data = request.get_json()
        newemail = data['newemail']
        randomNumber = data['randomnumber']
        if randomNumber != session['randomNumber']:
            return jsonify({'err':'验证码错误'})
        else:
            res = Userreset.updateemail(session['username'],newemail)       #更新数据库邮箱
            if res == 0:
                session['email'] = newemail
                session.pop('randomNumber')
                return jsonify({'err':0})
            else:
                return jsonify({'err':'后台错误！'})