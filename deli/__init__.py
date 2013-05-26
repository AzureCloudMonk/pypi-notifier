from flask import Flask
from flask import g, session, request, url_for, redirect, flash, render_template

import deli.config
from cache import cache
from views import register_views
from github import github
from models import db, User


def create_app(config):
    app = Flask(__name__)
    load_config(app, config)
    db.init_app(app)
    cache.init_app(app)
    github.init_app(app)
    register_views(app)

    @app.before_request
    def set_user():
        g.user = None
        if session.get('user_id', None):
            g.user = User.query.get(session['user_id'])

    @app.after_request
    def remove_session(response):
        db.session.remove()
        return response

    @github.access_token_getter
    def get_github_token():
        user = g.user
        if user is not None:
            return user.github_token

    @app.route('/github-callback')
    @github.authorized_handler
    def oauth_authorized(resp):
        next_url = request.args.get('next') or url_for('repos')

        if resp is None:
            flash('You denied the request to sign in.')
            return redirect(next_url)

        token = resp['access_token']
        user_response = github.get('user', params={'access_token': token})
        github_id = user_response['id']
        user = User.query.filter_by(github_token=token).first()
        if user is None:
            user = User.query.filter_by(github_id=github_id).first()
        if user is None:
            user = User(token)
            db.session.add(user)

        user.github_token = token
        user.github_id = github_id
        user.name = user_response['login']
        user.email = user_response['email']
        db.session.commit()
        session['user_id'] = user.id
        return redirect(next_url)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login')
    def login():
        if session.get('user_id', None) is None or g.user is None:
            return github.authorize(scope='user:email, public_repo')
        else:
            return redirect(url_for('index'))

    @app.route('/logout')
    def logout():
        session.pop('user_id', None)
        return redirect(url_for('index'))

    return app


def load_config(app, config):
    if isinstance(config, basestring):
        config = getattr(deli.config, config)
    app.config.from_object(config)
