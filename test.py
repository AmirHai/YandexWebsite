from flask import Flask, render_template, redirect, request
from werkzeug.exceptions import abort
from flask_login import current_user, login_user, LoginManager, logout_user, login_required
from data.user import User
from data.question import Question
from data import db_session
from forms.login import LoginForm
from forms.question import QuestionForm
from forms.register import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/question/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_question(id):
    form = QuestionForm()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        question = db_sess.query(Question).filter(Question.id == id,
                                                  Question.user == current_user).first()
        if question:
            form.title.data = question.title
            form.content.data = question.content
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        question = db_sess.query(Question).filter(Question.id == id,
                                                  Question.user == current_user).first()
        if question:
            question.title = form.title.data
            question.content = form.content.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('question.html', form=form, title='Редактирование вопроса')


@app.route('/question_delete/<int:id>', methods=['GET', 'POST'])
def delete_question(id):
    db_sess = db_session.create_session()
    question = db_sess.query(Question).filter(Question.id == id,
                                              Question.user == current_user).first()
    if question:
        db_sess.delete(question)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/question',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = QuestionForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        question = Question()
        question.title = form.title.data
        question.content = form.content.data
        current_user.questions.append(question)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('question.html', title='Добавление вопроса',
                           form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают",
                                   current_user=current_user)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть",
                                   current_user=current_user)
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form, current_user=current_user)


@app.route('/')
def index():
    db_sess = db_session.create_session()
    question = []
    if current_user.is_authenticated:
        question = db_sess.query(Question).filter(Question.user == current_user)
    else:
        redirect('/login')
    return render_template('index.html', question=question, current_user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
    return render_template('login.html', title="Авторизация", form=form,
                           current_user=current_user)


if __name__ == '__main__':
    db_session.global_init('db/forum.db')
    app.run()
