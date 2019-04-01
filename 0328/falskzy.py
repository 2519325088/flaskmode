from flask import Flask,redirect,render_template,request,make_response
import datetime,sqlalchemy
import splb,pymysqlcz
app=Flask(__name__)

from sqlalchemy.orm import sessionmaker
Session=sessionmaker(bind=pymysqlcz.engine)()



#页面控制部分
# 首页
@app.route('/',methods=['GET','POST'])
def index():
    # if request.method=='GET':
    user = None
    user = request.cookies.get("name")

    return render_template("index.html",user=user)


#注册
@app.route('/zhuce',methods=['GET','POST'])
def zhuce():
    if request.method=='GET':
        return render_template('zhuce.html')
    elif request.method=='POST':
        username = request.form['username']
        password = request.form['password']

        try:
            # # 判断是否有此账号
            result=Session.query(pymysqlcz.User).filter(pymysqlcz.User.username==username).first().id
            print(result, '=======0')
            if result:
                #若有此账号就重新注册
                print(result,'=======1')
                return render_template('zhuce.html',cunzai=[1])
            else:
                return redirect('/denglu')
        except:
            try:
                T1 =pymysqlcz.User(id=0, username=username, passwd=password)
                Session.add(T1)
                Session.commit()
                Session.close()
                return redirect('/denglu')
            except:
                Session.rollback()
                Session.close()



#登录
@app.route('/denglu',methods=['GET','POST'])
def denglu():
    if request.method=='GET':
        return render_template('denglu.html')
    elif request.method=='POST':
        username = request.form["username"]
        password = request.form['password']
        try:
            #判断账户密码是否存在
            result = Session.query(pymysqlcz.User).filter(pymysqlcz.User.username == username).filter(pymysqlcz.User.passwd == password).first().id
            if result:
                # 存在就进入商品页
                res = make_response(redirect("/shangpin"))
                res.set_cookie('name', username, expires=datetime.datetime.now() + datetime.timedelta(days=7))
                return res
            else:
                return render_template('denglu.html')
        except:
            try:
                return render_template('denglu.html',bucun=[1])
            except:
                Session.rollback()
                Session.close()



@app.route('/exita')
def quit():
    res=make_response(redirect('/'))
    res.delete_cookie('name')
    return res


#商品
@app.route('/shangpin',methods=['GET','POST'])
def shangpin():
    if request.method=='GET':
        user = None
        user = request.cookies.get("name")
        usera=Session.query(pymysqlcz.User).filter(pymysqlcz.User.username==user).first().id
        resul = Session.query(pymysqlcz.Splist).filter(pymysqlcz.Splist.userid==usera).all()
        # print(resul)
        return render_template('shangpin.html',user=user,resul=resul)



#添加
@app.route('/tianjia',methods=['GET','POST'])
def tianjia():
    if request.method=='GET':
        return render_template('tianjia.html')
    elif request.method=='POST':
        biaoti = request.form["biaoti"]
        neirong = request.form['neirong']
        user = request.cookies.get("name")
        resul = Session.query(pymysqlcz.User).filter(pymysqlcz.User.username==user).first().id
        T1 = pymysqlcz.Splist(id=0, spname=biaoti, nrtext=neirong,userid=resul)
        Session.add(T1)
        Session.commit()
        Session.close()
        return redirect('/shangpin')
        # return "hello"


#删除
@app.route('/shanchu/<id>')
def shanchu(id):
    Session.query(pymysqlcz.Splist).filter(pymysqlcz.Splist.spname==id).delete()
    Session.commit()
    Session.close()
    return redirect('/shangpin')


#修改
@app.route('/xiugai<namea>',methods=['GET','POST'])
def xiugai(namea):
    if request.method=='GET':
        return render_template('xiugai.html')
    elif request.method=='POST':
        user = None
        shuid = Session.query(pymysqlcz.Splist).filter(pymysqlcz.Splist.spname ==namea).first().userid
        user = request.cookies.get("name")
        useraa=Session.query(pymysqlcz.User).filter(pymysqlcz.User.id ==shuid).first().username
        if useraa==user:
            biaoti = request.form["biaoti"]
            neirong = request.form['neirong']
            # stra=nameb.split("'")[1]
            resul = Session.query(pymysqlcz.Splist).filter(pymysqlcz.Splist.spname==namea).first().id
            Session.query(pymysqlcz.Splist).filter(pymysqlcz.Splist.id==resul).first().spname=biaoti
            Session.query(pymysqlcz.Splist).filter(pymysqlcz.Splist.id== resul).first().nrtext=neirong
            Session.commit()
            Session.close()
            return redirect('/shangpin')
        else:
            return redirect('/shangpin')



#查看
@app.route('/chakan/<id>')
def chakan(id):
    resul = Session.query(pymysqlcz.Splist).filter(pymysqlcz.Splist.spname == id).first().nrtext
    return render_template('chakan.html',spname=id,texta=resul)

if __name__ =="__main__":
    app.run()



