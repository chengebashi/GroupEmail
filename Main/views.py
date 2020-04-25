__author__ = 'Chenge'
from . import *

@Main.route('/',methods=['GET','POST'])
def index():
    '''发送邮件主页'''
    if request.method == 'GET':
        uname = session.get('username')      #判断用户名seesion是否存在，若存在跳转主页，否则跳转登陆界面
        if not uname:
            return redirect('admin/login')
        else:
            img = session['head'] + '?r=' + str(sendemail.randomnumber())  #防止照片缓存
            return render_template('Main/index.html',img=img,uname=session['username'],nowtime=session['time'],email=session['email'])

    else:
        '''从草稿箱进入主页'''
        roughID = request.form.get('roughID')
        emailthesave = Useremail.resetRoughemail(roughID)
        img = session['head'] + '?r=' + str(sendemail.randomnumber())  # 防止照片缓存
        return render_template('Main/index.html', img=img, uname=session['username'], nowtime=session['time'],email=session['email'], emailsave=emailthesave)



@Main.route('/emaillist',methods=['GET','POST'])
def emaillist():
    '''邮件列表'''
    if request.method == 'GET':
        uname = session.get('username')      #判断用户名seesion是否存在，若存在跳转主页，否则跳转登陆界面
        if not uname:
            return redirect('admin/login')
        else:
            img = session['head'] + '?r=' + str(sendemail.randomnumber())
            emaillist = Useremail.showemails(session['username'])      #从数据库查询所有的邮件
            return render_template('Main/emaillist.html',imgpath=img, img=img, uname=session['username'], nowtime=session['time'],email=session['email'],emaillist=emaillist)

    else:
        pass

@Main.route('/sendEmail',methods=['POST'])
def sendEmail():
    '''发送邮件按钮'''
    data = request.get_json()
    receivers = [i.strip() for i in data['receivers']]
    receivers = list(set(receivers))
    title = data['title']
    content = data['content']
    response = sendemail.email_send(title,content,receivers) #群发邮件
    if response == 0:
        res = Useremail.insertemail(session['username'],receivers,title,content,session['head'])  #发送成功的邮件信息写入数据库
        if res == 1:
            return jsonify({'err':'数据库错误!'})
        else:
            return jsonify({'err':0})
    else:
        return jsonify({'err':'发送失败，请检查收件人邮箱地址是否存在！'})


@Main.route('/loading')
def loading():
    '''加载页面'''
    return render_template('Main/loading.html')

@Main.route('/movebin',methods=['POST'])
def movebin():
    '''写入垃圾箱'''
    data = request.get_json()
    emaillistID = data['id']
    # eid = 'e'+ emaillistID
    emailinfo = Useremail.showEmailBin(emaillistID)   #拿到被删除邮件信息
    res = Useremail.insertBinemaillist(emailinfo)  #被删除邮件写入垃圾箱
    if res == 1:
        return jsonify({'err':'数据库错误，无法写入垃圾箱！'})
    else:
        reg = Useremail.deleteemail_list(emaillistID)  #邮件列表删除此邮件
        if reg == 1:
            return jsonify({'err':'数据库错误，无法删除邮件！'})
        else:
            return jsonify({'err':0})


@Main.route('/emailBin',methods=['GET','POST'])
def emailBin():
    '''垃圾箱界面'''
    if request.method == 'GET':
        uname = session.get('username')  # 判断用户名seesion是否存在，若存在跳转主页，否则跳转登陆界面
        if not uname:
            return redirect('admin/login')
        else:
            img = session['head'] + '?r=' + str(sendemail.randomnumber())
            emailBinist = Useremail.showBin(session['username'])   #查询垃圾箱中此用户的邮件
            return render_template('Main/emailBin.html',imgpath=img, img=img,uname=session['username'],nowtime=session['time'],email=session['email'],emaillist=emailBinist)
    else:
        data = request.get_json()
        emailBinlistID = data['id']
        res = Useremail.deleteBinemail(emailBinlistID)  #删除垃圾箱中邮件
        if res == 0:
            return jsonify({'err':0})
        else:
            return jsonify({'err':'邮件无法删除，系统错误!'})


@Main.route('/saveEmail',methods=['POST'])
def saveEmail():
    '''保存邮件'''
    data = request.get_json() #获取前端发送过来的数据
    receivers = [i.strip() for i in data['receivers']]
    receivers = list(set(receivers))
    title = data['title']
    content = data['content']
    flag = data['flag']
    if not flag:
        res = Useremail.insertemailRough(session['username'], receivers, title, content, session['head'])  # 保存成功的邮件信息写入数据库
        if res == 0:
            return jsonify({'err':0})
        else:
            return jsonify({'err':'保存失败'})
    else:
        res = Useremail.updateRoughemail(flag, receivers, title, content)  # 保存成功的邮件信息写入数据库
        if res == 0:
            return jsonify({'err':0})
        else:
            return jsonify({'err':'保存失败，数据库错误!'})

@Main.route('/emailRough',methods=['GET'])
def emailRough():
    '''展示草稿箱邮件'''
    uname = session.get('username')  # 判断用户名seesion是否存在，若存在跳转主页，否则跳转登陆界面
    if not uname:
        return redirect('admin/login')
    else:
        img = session['head'] + '?r=' + str(sendemail.randomnumber())
        emailBinist = Useremail.showRoughemail(session['username'])  # 查询垃圾箱中此用户的邮件
        return render_template('Main/emailRough.html',imgpath=img, img=img,uname=session['username'],nowtime=session['time'],email=session['email'],emaillist=emailBinist)

@Main.route('/deleteRoughemail', methods=['POST'])
def deleteRoughemail():
    '''删除草稿箱邮件'''
    data = request.get_json()
    emailBinlistID = data['id']
    res = Useremail.deleteRough(emailBinlistID)  # 删除垃圾箱中邮件
    if res == 0:
        return jsonify({'err': 0})
    else:
        return jsonify({'err': '邮件无法删除，系统错误!'})