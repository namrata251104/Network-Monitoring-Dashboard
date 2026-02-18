from flask import Blueprint, render_template, request, jsonify
from models.database import db, LoginLog, Alert
from datetime import datetime, timedelta
import random

logs_bp = Blueprint('logs', __name__)

@logs_bp.route('/logs')
def logs_page():
    return render_template('logs.html')

@logs_bp.route('/api/logs')
def get_logs():
    log_type = request.args.get('type', 'all')
    severity = request.args.get('severity', 'all')
    date_range = request.args.get('date_range', '1')
    search = request.args.get('search', '')
    
    # Generate sample logs if database is empty
    logs = []
    
    # Add login logs
    for i in range(10):
        logs.append({
            'id': i + 1,
            'timestamp': (datetime.now() - timedelta(hours=random.randint(0, 24))).strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'login',
            'severity': 'info' if random.random() > 0.2 else 'warning',
            'message': f'User {"admin" if random.random() > 0.3 else "unknown"} {"login successful" if random.random() > 0.2 else "login failed"}',
            'source': 'auth_system'
        })
    
    # Add system alerts
    for i in range(15):
        severity_options = ['info', 'warning', 'error', 'critical']
        messages = [
            'CPU usage exceeded threshold',
            'Memory usage high',
            'Disk space low',
            'Network connection lost',
            'Service restarted',
            'Backup completed',
            'System update available'
        ]
        
        logs.append({
            'id': i + 11,
            'timestamp': (datetime.now() - timedelta(hours=random.randint(0, 48))).strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'alerts',
            'severity': random.choice(severity_options),
            'message': random.choice(messages),
            'source': 'system_monitor'
        })
    
    # Add system events
    for i in range(8):
        logs.append({
            'id': i + 26,
            'timestamp': (datetime.now() - timedelta(hours=random.randint(0, 72))).strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'system',
            'severity': 'info',
            'message': f'System {"startup" if i == 0 else "shutdown" if i == 1 else "check completed"}',
            'source': 'system'
        })
    
    # Apply filters
    if log_type != 'all':
        logs = [log for log in logs if log['type'] == log_type]
    
    if severity != 'all':
        logs = [log for log in logs if log['severity'] == severity]
    
    if search:
        logs = [log for log in logs if search.lower() in log['message'].lower()]
    
    # Sort by timestamp (newest first)
    logs.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return jsonify(logs)

@logs_bp.route('/api/logs/stats')
def get_logs_stats():
    stats = {
        'info': 12,
        'warning': 8,
        'error': 3,
        'critical': 1
    }
    return jsonify(stats)
