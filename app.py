from flask import Flask, render_template, session
from models.database import db, init_database
from routes.auth import auth_bp
from routes.main import main_bp
from routes.api import api_bp
from routes.logs import logs_bp
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(api_bp)
app.register_blueprint(logs_bp)

@app.template_filter('format_bytes')
def format_bytes(bytes_value):
    if bytes_value == 0:
        return "0 B"
    
    units = ["B", "KB", "MB", "GB", "TB"]
    unit_index = 0
    
    while bytes_value >= 1024 and unit_index < len(units) - 1:
        bytes_value /= 1024
        unit_index += 1
    
    return f"{bytes_value:.1f} {units[unit_index]}"

@app.template_filter('format_percentage')
def format_percentage(value):
    return f"{value:.1f}%"

@app.template_filter('format_uptime')
def format_uptime(seconds):
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    
    if days > 0:
        return f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        init_database(app)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
