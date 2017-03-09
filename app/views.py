from flask import render_template,flash,redirect,session,url_for,request, g
from . import app, lm, db
from .forms import LoginForm
from flask_login import login_user, logout_user, current_user, login_required
from .models import User
from datetime import datetime
from .forms import LoginForm,EditForm


@app.route('/')
@app.route('/index', methods=['GET'])
@login_required
def index():
    user = g.user
    posts =[
            {   'author':{'nickname':'john'},
                'body': 'Beautiful day in Portland!',
                'avatar':'https://pickaface.net/assets/images/slides/slide4.png'
            },
            {    'author':{'nickname':'susan'},
                 'body':'The Avengers movie was so cool!',
                 'avatar':'https://pickaface.net/assets/images/slides/slide4.png'

    }
    ]
    return render_template('index.html', title="Home", user=user, posts=posts)


@app.route('/login',methods=['GET','POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            session['username'] = form.username.data
            session['remember_me'] = form.remember_me.data
            g.user = user
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('user', nickname=user.nickname))
        else:
            flash("User not found")
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash('User %s not found.'% nickname)
        return redirect(url_for('index'))
    posts = [
        {'author': user,'body': 'Test post #1'},
        {'author': user,'body': 'Test post #2'}
    ]
    return render_template('user.html',user=user,posts=posts)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@app.route('/after_login')
@login_required
@app.before_request
def before_request():
    g.user = current_user


def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            # nickname = resp.email.split('@')[0]
            nickname = User.make_unique_nickname(nickname)
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/edit', methods=['GET','POST'])
@login_required
def edit():
     form = EditForm(g.user.nickname)
     if form.validate_on_submit():
         g.user.nickname = form.nickname.data
         g.user.about_me = form.about_me.data
         db.session.add(g.user)
         db.session.commit()
         flash('Your changes have been saved.')
         return redirect(url_for('user', nickname=g.user.nickname))
     else:
         form.nickname.data = g.user.nickname
         form.about_me.data = g.user.about_me
     return render_template('edit.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash(u'You were signed out')
    return redirect(url_for('login'))

@app.errorhandler(404)
def not_found_error(error):
     return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
     db.session.rollback()
     return render_template('500.html'), 500
