from flask import Blueprint, jsonify, session
from utils.system_monitor import SystemMonitor
from models.database import db, Alert
from datetime import datetime
import random

api_bp = Blueprint('api', __name__, url_prefix='/api')
system_monitor = SystemMonitor()

@api_bp.route('/cpu')
def get_cpu():
    data = system_monitor.get_cpu_usage()
    return jsonify(data)

@api_bp.route('/ram')
def get_ram():
    data = system_monitor.get_ram_usage()
    return jsonify(data)

@api_bp.route('/disk')
def get_disk():
    data = system_monitor.get_disk_usage()
    return jsonify(data)

@api_bp.route('/network')
def get_network():
    data = system_monitor.get_network_activity()
    return jsonify(data)

@api_bp.route('/processes')
def get_processes():
    data = system_monitor.get_processes()
    return jsonify(data)

@api_bp.route('/system-info')
def get_system_info():
    data = system_monitor.get_system_info()
    return jsonify(data)

@api_bp.route('/alerts')
def get_alerts():
    current_alerts = system_monitor.check_alerts()
    
    for alert_data in current_alerts:
        existing_alert = Alert.query.filter_by(
            alert_type=alert_data['type'],
            resolved=False
        ).first()
        
        if not existing_alert:
            new_alert = Alert(
                alert_type=alert_data['type'],
                message=alert_data['message'],
                severity=alert_data['severity']
            )
            db.session.add(new_alert)
    
    unresolved_alerts = Alert.query.filter_by(resolved=False).order_by(Alert.created_at.desc()).all()
    
    alert_list = []
    for alert in unresolved_alerts:
        alert_list.append({
            'id': alert.id,
            'type': alert.alert_type,
            'message': alert.message,
            'severity': alert.severity,
            'created_at': alert.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify(alert_list)

@api_bp.route('/resolve-alert/<int:alert_id>')
def resolve_alert(alert_id):
    alert = Alert.query.get_or_404(alert_id)
    alert.resolve()
    db.session.commit()
    return jsonify({'success': True})

@api_bp.route('/all-metrics')
def get_all_metrics():
    return jsonify({
        'cpu': system_monitor.get_cpu_usage(),
        'ram': system_monitor.get_ram_usage(),
        'disk': system_monitor.get_disk_usage(),
        'network': system_monitor.get_network_activity(),
        'processes': system_monitor.get_processes(),
        'system_info': system_monitor.get_system_info(),
        'timestamp': datetime.now().isoformat()
    })

@api_bp.route('/historical-data')
def get_historical_data():
    historical_data = {
        'cpu': [],
        'ram': [],
        'disk': [],
        'network': []
    }
    
    for i in range(20):
        timestamp = datetime.now().timestamp() - (19 - i) * 120
        
        cpu_data = system_monitor.get_cpu_usage()
        ram_data = system_monitor.get_ram_usage()
        disk_data = system_monitor.get_disk_usage()
        network_data = system_monitor.get_network_activity()
        
        historical_data['cpu'].append({
            'timestamp': timestamp,
            'value': cpu_data['percentage']
        })
        
        historical_data['ram'].append({
            'timestamp': timestamp,
            'value': ram_data['percentage']
        })
        
        historical_data['disk'].append({
            'timestamp': timestamp,
            'value': disk_data['percentage']
        })
        
        historical_data['network'].append({
            'timestamp': timestamp,
            'upload': network_data['upload_speed'],
            'download': network_data['download_speed']
        })
    
    return jsonify(historical_data)
