import datetime

from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user
from forms.user import RegisterForm, LoginForm
from faker import Faker
from forms.job import JobForm
from mars.data import db_session
from mars.data.jobs import Jobs
from mars.data.users import User

f = Faker()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("index.html", jobs=jobs)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm()
    return render_template('add_job.html', title='Добавить работу', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


def main():
    db_session.global_init("db/mars_explorer.db")

    db_sess = db_session.create_session()
    for i in range(5, 8):
        user_data = {
            'surname': f.last_name(),
            'name': f.first_name(),
            'age': f.random_int(20, 60),
            'position': 'captain' if i == 0 else f.job(),
            'speciality': f.job(),
            'address': 'module_1',
            'email': f.email()
        }
        user = User(**user_data)
        db_sess.add(user)
    job_data = {
        'team_lead': 1,
        'job': f.job(),
        'work_size': f.random_int(1, 20),
        'collaborators': '3, 4',
        'start_date': datetime.datetime.now(),
        'is_finished': False
    }
    job = Jobs(**job_data)
    db_sess.add(job)
    db_sess.commit()
    app.run()


if __name__ == '__main__':
    main()
