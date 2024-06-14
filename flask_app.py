# 필수 라이브러리
'''
0. Flask : 웹서버를 시작할 수 있는 기능. app이라는 이름으로 플라스크를 시작한다
1. render_template : html파일을 가져와서 보여준다
'''
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, render_template, request, redirect, url_for, flash 
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user 
from sqlalchemy import or_
app = Flask(__name__)
# DB 기본 코드

app = Flask(__name__)

# login
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # main
# app.config['SQLALCHEMY_DATABASE_URI'] =\
#         'sqlite:///' + os.path.join(basedir, 'database.db')


db = SQLAlchemy(app)

# main


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    imgUrl = db.Column(db.String(10000), nullable=False)


# login
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    level = db.Column(db.Integer, nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    item_list = Items.query.all()
    return render_template('home.html', data=item_list)


@app.route("/mnt/")
def mnt():
    item_list = Items.query.all()
    return render_template('manager.html', data=item_list)

@app.route("/mnt2/")
def mnt2():
    item_list = Items.query.all()
    return render_template('manager2.html', data=item_list)

@app.route("/mnt1/")
def mnt1():
    item_list = Items.query.all()
    return render_template('manager1.html', data=item_list)




@app.route("/mnt/create/", methods=["POST"])
def item_create():
    # form에서 보낸 데이터 받아오기
    name_receive = request.form.get("name")
    price_receive = request.form.get("price")
    count_receive = request.form.get("count")
    imgUrl_receive = request.form.get("imgUrl")

    # 데이터를 DB에 저장하기
    item = Items(name=name_receive, price=price_receive,
                count=count_receive, imgUrl=imgUrl_receive)
    db.session.add(item)
    db.session.commit()

    return redirect(url_for('mnt'))


@app.route("/mnt/delete/", methods=["POST"])
def item_del():

    id_receive = request.form.get("item_id")
    item_id_nm = Items.query.filter_by(id=id_receive).first()

    db.session.delete(item_id_nm)
    db.session.commit()

    return redirect(url_for('mnt'))


@app.route("/mnt/add/", methods=["POST"])
def item_add():

    id_receive = request.form.get("item_id")
    item_id_nm = Items.query.filter_by(id=id_receive).first()

    if item_id_nm:
        item_id_nm.count += 1
        db.session.commit()

    return redirect(url_for('mnt'))
        


@app.route("/mnt/sub/", methods=["POST"])
def item_sub():

    id_receive = request.form.get("item_id")
    item_id_nm = Items.query.filter_by(id=id_receive).first()

    if item_id_nm:
        item_id_nm.count -= 1
        db.session.commit()

    return redirect(url_for('mnt'))

@app.route("/mnt/search_h/", methods=["GET"])
def item_search_h():
    search_receive = request.args.get("search", "")
    search_list = Items.query.filter(
        or_(Items.name.like(f'%{search_receive}%'))).all()
        
    return render_template('home.html', data=search_list)

@app.route("/mnt/search_m/", methods=["GET"])
def item_search_m():
    search_receive = request.args.get("search", "")
    search_list = Items.query.filter(
        or_(Items.name.like(f'%{search_receive}%'))).all()
        
    return render_template('manager.html', data=search_list)


####################################################################################

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            if user and user.level == 3:
                login_user(user)
                return redirect(url_for('mnt'))
            elif user and user.level == 2:
                login_user(user)
                return redirect(url_for('mnt2'))
            elif user and user.level == 1:
                login_user(user)
                return redirect(url_for('mnt1'))            
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/login_index')
@login_required
def login_index():
    return render_template('login_index.html', username=current_user.username)

@app.route("/mnt/login_create/", methods=["POST"])
def login_create():
    # form에서 보낸 데이터 받아오기
    username_receive = request.form.get("username")
    name_receive = request.form.get("name")
    password_receive = request.form.get("password")
    level_receive = request.form.get("level")

    # 데이터를 DB에 저장하기
    login_id = User(username=username_receive, name=name_receive, password=password_receive, level=level_receive)
    db.session.add(login_id)
    db.session.commit()

    return redirect(url_for('mnt'))


if __name__ == "__main__":
    app.run(debug=True)

