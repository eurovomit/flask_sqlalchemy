from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)


class KG (db.Model):
    __tablename__ = 'kg'
    # ограничение первичного ключа
    id = db.Column(db.Integer, primary_key=True)
    # ограничение на пустое значение
    name = db.Column(db.String(32), nullable=False)
    # ограничение CHECK
    town = db.Column(db.String(32), db.CheckConstraint('town is not NULL'))
    group = relationship('Group')


class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    # ограничение вторичного ключа
    kg_id = db.Column(db.Integer, db.ForeignKey('kg.id'))
    kg = relationship('KG')


# удалить все таблицы
with app.app_context():
    db.drop_all()

# в новых версиях нужно вызывать через контекст
# создать таблицы из классов
with app.app_context():
    db.create_all()

kg111 = KG(name='111', town='KLD')
kg112 = KG(name='112', town='KLD')
kg113 = KG(name='113', town='Svetliy')
kg114 = KG(name='114', town='Baltiysk')

kg115 = KG(name='115', town='KLD')
group_small = Group(name='младшая', kg=kg115)


with app.app_context():
    # первый способ добавления записей
    db.session.add(kg111)
    db.session.add(kg112)
    db.session.add(kg115)
    db.session.add(group_small)
    # второй способ добавления записей
    kgs = [kg113, kg114]
    db.session.add_all(kgs)
    # показать недобавленные, но готовые к записи
    print(db.session.new)
    # записать в БД
    db.session.commit()


# получаем первую запись из таблицы
@app.route('/kg/first')
def get_first_kg():
    kg = KG.query.first()
    return str(kg.id) + ' ' + kg.name + ' ' + kg.town


# получаем число записей
@app.route('/kg/count')
def get_count_kg():
    kg = KG.query.count()
    return str(kg)


# получаем все записи из таблицы
@app.route('/kgs')
def get_kgs():
    kgs = KG.query.all()
    kgs_list = []
    for kg in kgs:
        kgs_list.append(str(kg.id) + ' ' + kg.name + ' ' + kg.town)
    return str(kgs_list)


# получаем запись из таблицы по id
@app.route('/kg/<int:sid>')
def get_kg(sid: int):
    kg = KG.query.get(sid)
    if kg is None:
        return 'kg not found'
    return str(kg.id) + ' ' + kg.name + ' ' + kg.town


if __name__ == '__main__':
    app.run(debug=True)
