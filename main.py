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
cur_user = 'Karim'


def add_user(name, university, delta, olp, achv):
    index = university.find('(')
    index2 = university.find(')')
    tmp_sl = university[index + 1:index2]
    unir = university[:index]
    if db_sess.query(University).filter(University.name == unir).count() < 1:
        print(f"{unir} Такого университет нет в списке.")
        return
    for tt in tmp_sl.split(','):
        tt = tt.replace(' ', '')
        fl = 0
        for un in db_sess.query(University).filter(University.name == unir):
            if un.faculty == tt:
                fl = 1
        if not fl:
            print(f"{tt} Такого факультета нет в {unir}.")
            return
    for i in olp.split(','):
        if db_sess.query(Olymps).filter(Olymps.name == i).count() < 1:
            print(f"{i} Такой олимпиады нет в списке.")
            return
    user = User()
    user.name = name
    user.university = university
    user.delta = delta
    user.olymps_list = olp
    user.achiv = achv
    db_sess.add(user)
    db_sess.commit()


def add_olymp(name, day, month, year, what_give):
    olmp = Olymps()
    olmp.name = name
    olmp.date = datetime.date(year, month, day)
    olmp.what_give = what_give
    db_sess.add(olmp)
    db_sess.commit()


def add_university(name, faculty, olmp, subjects):
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


def user_university_add(university):
    global db_sess
    index = university.find('(')
    index2 = university.find(')')
    tmp_sl = university[index + 1:index2]
    unir = university[:index]
    if db_sess.query(University).filter(University.name == unir).count() < 1:
        print(f"{unir} Такого университет нет в списке.")
        return
    for tt in tmp_sl.split(','):
        tt = tt.replace(' ', '')
        fl = 0
        for un in db_sess.query(University).filter(University.name == unir):
            if un.faculty == tt:
                fl = 1
        if not fl:
            print(f"{tt} Такого факультета нет в {unir}.")
            return
    tmp_user = db_sess.query(User).filter(User.name == cur_user)[0]
    tmp_user_univ = tmp_user.university.split(')')
    counter = 0
    fl = 0
    for tmp_un in tmp_user_univ:
        ind_tmp_un = tmp_un.find('(')
        if tmp_un[:ind_tmp_un] == unir:
            fl = 1
            tmp_user_univ[counter] += f', {tmp_sl}'
        counter += 1
    tmp_user_univ = ')'.join(tmp_user_univ)
    if fl == 0:
        tmp_user_univ += f', {university}'
    user = User()
    user.name = tmp_user.name
    user.university = tmp_user_univ
    user.delta = tmp_user.delta
    user.olymps_list = tmp_user.olymps_list
    user.achiv = tmp_user.achiv
    db_sess.delete(tmp_user)
    db_sess.add(user)
    db_sess.commit()

def user_university_delete(univers):
    tmp_user = db_sess.query(User).filter(User.name == cur_user)[0]
    tmp_user_univer = tmp_user.university
    index = tmp_user_univer.find(univers)
    tmp_index = index
    alph = ['abcdefghijklmnopqrstuvwxyz']
    while tmp_user_univer[tmp_index] != ')':
        tmp_index += 1
    while tmp_index < len(tmp_user_univer) - 1 and not (tmp_user_univer[tmp_index] in alph):
        tmp_index += 1
    tmp_user_univer = tmp_user_univer[:index] + tmp_user_univer[tmp_index + 1:]
    user = User()
    user.name = tmp_user.name
    user.university = tmp_user_univer
    user.delta = tmp_user.delta
    user.olymps_list = tmp_user.olymps_list
    user.achiv = tmp_user.achiv
    db_sess.delete(tmp_user)
    db_sess.add(user)
    db_sess.commit()



def user_change_achiv(achv):
    pass


def user_add_olymp(olymp):
    pass
def user_olymp_delete(univers):
    pass

def user_change_delta(delta, olymp):
    pass

def get_university():
    pass

def get_olymp():
    pass

def delete_all():
    for i in db_sess.query(Olymps).filter():
        db_sess.delete(i)
        db_sess.commit()
    for i in db_sess.query(University).filter():
        db_sess.delete(i)
        db_sess.commit()
    for i in db_sess.query(User).filter():
        db_sess.delete(i)
        db_sess.commit()


def main():
    global cur_user
    delete_all()
    Ol = [('Всерос по инфе', 13, 12, 2024, 'БВИ в любой ВУЗ')]
    unive = [('МФТИ', 'ПМИ', 'Всерос по инфе', 'Математика, Информатика'), ('МФТИ', 'jkl', 'Всерос по инфе', 'Математика, Информатика')]
    usr = [('Карим', "МФТИ(ПМИ)", 2, 'Всерос по инфе', 'Обладаю слепой печатью')]
    cur_user = 'Карим'
    add_olymp(*Ol[0])
    add_university(*unive[0])
    add_university(*unive[1])
    add_user(*usr[0])
    user_university_add('МФТИ(jkl)')
    add_user(*usr[0])
    user_university_delete('МФТИ')
    print("Olymps")
    for ol in db_sess.query(Olymps).filter():
        print(ol.name, ol.date, ol.what_give)
    print("University")
    for univer in db_sess.query(University).filter():
        print(univer.name, univer.olymps_list, univer.subjects, univer.faculty)
    print("User")
    for usr in db_sess.query(User).filter():
        print(usr.name, usr.university, usr.delta, usr.olymps_list, usr.achiv)

    #app.run()


if __name__ == '__main__':
    main()