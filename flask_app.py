# 필수 라이브러리
'''
0. Flask : 웹서버를 시작할 수 있는 기능. app이라는 이름으로 플라스크를 시작한다
1. render_template : html파일을 가져와서 보여준다
'''
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
# DB 기본 코드
import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)

class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    imgUrl = db.Column(db.String(10000), nullable=False)

    # def __repr__(self):
    #     return f'{self.username} {self.title} 추천 by {self.username}'

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

@app.route("/mnt/create/", methods=["POST"])
def item_create():
    # form에서 보낸 데이터 받아오기
    name_receive = request.form.get("name")
    price_receive = request.form.get("price")
    count_receive = request.form.get("count")
    imgUrl_receive = request.form.get("imgUrl")

    # 데이터를 DB에 저장하기
    item = Items(name=name_receive, price=price_receive, count=count_receive, imgUrl=imgUrl_receive)
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


if __name__ == "__main__":
    app.run(debug=True)

