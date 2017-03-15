from flask import render_template,flash,redirect,session,url_for,request, g
from app import app, lm, db
from flask_login import login_user, logout_user, current_user, login_required
from .models import User,Post
from datetime import datetime
from .forms import LoginForm,EditForm,PostForm,SearchForm
from config import POSTS_PER_PAGE
from config import MAX_SEARCH_RESULTS
from .emails import follower_notification

import models

@app.route('/',methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
@login_required
def index(page=1):
    form = PostForm()
    user = g.user
    if form.validate_on_submit():
        post = Post(body=form.post.data, user_id=g.user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        # return redirect(url_for('index'))
    posts = db.session.query(models.Post).paginate(page, POSTS_PER_PAGE, False)
    #print g.user.followed_posts(), posts.items
    return render_template('index.html', title="Home", form=form,user=user, posts=posts)


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
@app.route('/user/<nickname>/<int:page>')
@login_required
def user(nickname,page=1):
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash('User %s not found.'% nickname)
        return redirect(url_for('index'))
    posts = user.posts.paginate(page,POSTS_PER_PAGE,False)
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
        g.search_form = SearchForm()


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
            nickname = resp.email.split('@')[0]
            nickname = User.make_unique_nickname(nickname)
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
        db.session.add(user.follow(user))
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

@app.route('/search', methods=['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('search_results',query=g.search_form.search.data))

@app.route('/search_results/<query>')
@login_required
def search_results(query):
    results =Post.query.whoosh_search(query,MAX_SEARCH_RESULTS).all()
    db.session.commit()
    return render_template('search_results.html', query=query, results=results, user=g.user)

@app.route('/userlist', methods=['GET', 'POST'])
@login_required
def userlist():
    userlist = User.query.all()
    return render_template('userlist.html', userlist=userlist)


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


@app.route('/follow/<username>', methods=['GET', 'POST'])
@login_required
def follow(username):
    if g.user == current_user:
        user = User.query.filter_by(username=username).first()
        u = g.user.follow(user)
        if u is None:
            flash("Can not follow " + username)
            return redirect(url_for('userlist'))
        db.session.add(u)
        db.session.commit()
    #return redirect(url_for('userlist'))
    follower_notification(user, g.user)
    flash('You are now following ' + username + '!')
    return redirect(url_for('userlist', username=username))


@app.route('/unfollow/<username>', methods=['GET','POST'])
@login_required
def unfollow(username):
    if g.user== current_user:
        user = User.query.filter_by(username=username).first()
        u= g.user.unfollow(user)
        if u is None:
            flash("Can not unfollow"+username)
            return redirect(url_for('userlist'))
        db.session.add(u)
        db.session.commit()
    return redirect(url_for('userlist'))
