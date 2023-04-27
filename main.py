from flask import Flask
from data import db_session
import datetime
from data.users import User
from data.olymps import Olymps
from data.university import University


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/olymps_university.db")
db_sess = db_session.create_session()


def add_user(name, university, faculty, delta, olp, achv):
    fl = 0
    if db_sess.query(University).filter(University.name == university).count() < 1:
        print(f"{university} Такого университет нет в списке.")
        return
    for uni in db_sess.query(University).filter(University.name == university):
        if uni.faculty == faculty:
            fl = 1
    if fl == 0:
        print(f"{faculty} Такого факультета нет в списке.")
        return
    for i in olp.split(','):
        if db_sess.query(Olymps).filter(Olymps.name == i).count() < 1:
            print(f"{i} Такой олимпиады нет в списке.")
            return
    user = User()
    user.name = name
    user.university = university
    user.faculty = faculty
    user.delta = delta
    user.olymps_list = olp
    user.achiv = achv
    db_sess.add(user)
    db_sess.commit()


def add_olymp(name, day, month, year, what_give):
    olmp = Olymps()
    olmp.name = name
    olmp.date = datetime.datetime(year, month, day)
    olmp.what_give = what_give
    db_sess.add(olmp)
    db_sess.commit()


def add_university(name, olmp, subjects, faculty):
    fl = 0
    for i in olmp.split(','):
        if db_sess.query(Olymps).filter(Olymps.name == i).count() < 1:
            print(f"{i} Такой олимпиады нет в списке.")
            return
    university = University()
    university.name = name
    university.olymps_list = olmp
    university.subjects = subjects
    university.faculty = faculty
    db_sess.add(university)
    db_sess.commit()

def main():
    Ol = [('Всерос по инфе', 13, 12, 2024, 'БВИ в любой ВУЗ')]
    unive = [('МФТИ', 'Всерос по инфе', 'Математика, Информатика', 'ПМИ')]
    usr = [('Карим', "МФТИ", 'ПМИ', 2, 'Всерос по инфе', 'Обладаю слепой печатью')]
    add_olymp(*Ol[0])
    add_university(*unive[0])
    add_user(*usr[0])
    print("Olymps")
    for ol in db_sess.query(Olymps).filter():
        print(ol.name, ol.date, ol.what_give)
    print("University")
    for univer in db_sess.query(University).filter():
        print(univer.name, univer.olymps_list, univer.subjects, univer.faculty)
    print("User")
    for usr in db_sess.query(User).filter():
        print(usr.name, usr.university, usr.faculty, usr.delta, usr.olymps_list, usr.achiv)

    #app.run()


if __name__ == '__main__':
    main()