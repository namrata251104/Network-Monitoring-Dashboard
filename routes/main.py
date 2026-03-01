from flask import Blueprint, render_template, session, redirect, url_for
from routes.auth import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@main_bp.route('/logs')
@login_required
def logs():
    return render_template('logs.html')
