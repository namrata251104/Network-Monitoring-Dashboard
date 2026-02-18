from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models.database import db, User, LoginLog
from datetime import datetime
import functools

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please enter both username and password', 'error')
            return render_template('login_simple.html')
        
        user = User.query.filter_by(username=username).first()
        
        login_log = LoginLog(
            user_id=user.id if user else None,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            success=False
        )
        
        if user and user.check_password(password) and user.is_active:
            session['user_id'] = user.id
            session['username'] = user.username
            login_log.user_id = user.id
            login_log.success = True
            db.session.add(login_log)
            db.session.commit()
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            db.session.add(login_log)
            db.session.commit()
            flash('Invalid username or password', 'error')
            return render_template('login_simple.html')
    
    return render_template('login_simple.html')

@auth_bp.route('/logout')
def logout():
    if 'user_id' in session:
        login_log = LoginLog(
            user_id=session['user_id'],
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            success=False
        )
        db.session.add(login_log)
        db.session.commit()
    
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/check-session')
def check_session():
    if 'user_id' in session:
        return jsonify({'logged_in': True, 'username': session['username']})
    return jsonify({'logged_in': False})
