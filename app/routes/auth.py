from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import login_user, logout_user, login_required, current_user
from app import db, oauth
from app.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('tasks.index'))
    redirect_uri = url_for('auth.callback', _external=True)
    return oauth.github.authorize_redirect(redirect_uri)


@auth_bp.route('/callback')
def callback():
    token = oauth.github.authorize_access_token()
    resp = oauth.github.get('user', token=token)
    user_info = resp.json()

    user = User.query.filter_by(github_id=user_info['id']).first()

    if not user:
        user = User(
            github_id=user_info['id'],
            username=user_info['login'],
            email=user_info.get('email'),
            avatar_url=user_info.get('avatar_url'),
        )
        db.session.add(user)
        db.session.commit()
        flash(f'Conta criada! Bem-vindo, {user.username}!', 'success')
    else:
        flash(f'Bem-vindo de volta, {user.username}!', 'success')

    login_user(user)
    return redirect(url_for('tasks.index'))


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu com sucesso.', 'info')
    return redirect(url_for('main.index'))
