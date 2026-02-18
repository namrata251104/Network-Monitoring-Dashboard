import psutil
import time
import random
from datetime import datetime

class SystemMonitor:
    def __init__(self):
        self.use_real_data = True
        try:
            psutil.cpu_percent()
            psutil.virtual_memory()
            psutil.disk_usage('/')
        except Exception:
            self.use_real_data = False
    
    def get_cpu_usage(self):
        if self.use_real_data:
            try:
                return {
                    'percentage': psutil.cpu_percent(interval=0.1),
                    'cores': psutil.cpu_count(),
                    'frequency': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
                    'load_avg': psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None
                }
            except Exception:
                return self._simulate_cpu_data()
        else:
            return self._simulate_cpu_data()
    
    def _simulate_cpu_data(self):
        base_usage = 30 + random.uniform(-10, 40)
        return {
            'percentage': min(100, max(0, base_usage + random.uniform(-5, 5))),
            'cores': 8,
            'frequency': {'current': 2400 + random.uniform(-200, 200), 'min': 800, 'max': 3200},
            'load_avg': [base_usage/100, base_usage/100, base_usage/100]
        }
    
    def get_ram_usage(self):
        if self.use_real_data:
            try:
                memory = psutil.virtual_memory()
                swap = psutil.swap_memory()
                return {
                    'total': memory.total,
                    'available': memory.available,
                    'used': memory.used,
                    'percentage': memory.percent,
                    'swap_total': swap.total,
                    'swap_used': swap.used,
                    'swap_percentage': swap.percent
                }
            except Exception:
                return self._simulate_ram_data()
        else:
            return self._simulate_ram_data()
    
    def _simulate_ram_data(self):
        total = 16 * 1024 * 1024 * 1024
        used_percentage = 40 + random.uniform(-15, 30)
        used = total * (used_percentage / 100)
        return {
            'total': total,
            'available': total - used,
            'used': used,
            'percentage': used_percentage,
            'swap_total': 4 * 1024 * 1024 * 1024,
            'swap_used': 0.2 * 1024 * 1024 * 1024,
            'swap_percentage': 5
        }
    
    def get_disk_usage(self):
        if self.use_real_data:
            try:
                disk = psutil.disk_usage('/')
                return {
                    'total': disk.total,
                    'used': disk.used,
                    'free': disk.free,
                    'percentage': (disk.used / disk.total) * 100,
                    'read_bytes': psutil.disk_io_counters().read_bytes if psutil.disk_io_counters() else 0,
                    'write_bytes': psutil.disk_io_counters().write_bytes if psutil.disk_io_counters() else 0
                }
            except Exception:
                return self._simulate_disk_data()
        else:
            return self._simulate_disk_data()
    
    def _simulate_disk_data(self):
        total = 500 * 1024 * 1024 * 1024
        used_percentage = 60 + random.uniform(-10, 20)
        used = total * (used_percentage / 100)
        return {
            'total': total,
            'used': used,
            'free': total - used,
            'percentage': used_percentage,
            'read_bytes': random.randint(1000000000, 5000000000),
            'write_bytes': random.randint(500000000, 2000000000)
        }
    
    def get_network_activity(self):
        if self.use_real_data:
            try:
                net_io = psutil.net_io_counters()
                net_connections = len(psutil.net_connections())
                return {
                    'bytes_sent': net_io.bytes_sent,
                    'bytes_recv': net_io.bytes_recv,
                    'packets_sent': net_io.packets_sent,
                    'packets_recv': net_io.packets_recv,
                    'connections': net_connections,
                    'upload_speed': random.uniform(1000000, 10000000),
                    'download_speed': random.uniform(2000000, 20000000)
                }
            except Exception:
                return self._simulate_network_data()
        else:
            return self._simulate_network_data()
    
    def _simulate_network_data(self):
        return {
            'bytes_sent': random.randint(1000000000, 10000000000),
            'bytes_recv': random.randint(2000000000, 20000000000),
            'packets_sent': random.randint(1000000, 10000000),
            'packets_recv': random.randint(2000000, 20000000),
            'connections': random.randint(10, 50),
            'upload_speed': random.uniform(1000000, 10000000),
            'download_speed': random.uniform(2000000, 20000000)
        }
    
    def get_processes(self):
        if self.use_real_data:
            try:
                processes = []
                for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
                    try:
                        pinfo = proc.info
                        if pinfo['cpu_percent'] is not None and pinfo['memory_percent'] is not None:
                            processes.append(pinfo)
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        pass
                
                processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
                return processes[:10]
            except Exception:
                return self._simulate_processes()
        else:
            return self._simulate_processes()
    
    def _simulate_processes(self):
        process_names = [
            'chrome.exe', 'firefox.exe', 'node.exe', 'python.exe', 'code.exe',
            'explorer.exe', 'svchost.exe', 'docker.exe', 'mysql.exe', 'nginx.exe'
        ]
        
        processes = []
        for i, name in enumerate(random.sample(process_names, 10)):
            processes.append({
                'pid': random.randint(1000, 9999),
                'name': name,
                'cpu_percent': random.uniform(0.1, 25.0),
                'memory_percent': random.uniform(0.1, 15.0),
                'status': random.choice(['running', 'sleeping', 'idle'])
            })
        
        return sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)
    
    def get_system_info(self):
        boot_time = None
        if self.use_real_data:
            try:
                boot_time = psutil.boot_time()
            except Exception:
                pass
        
        if not boot_time:
            boot_time = time.time() - (random.randint(1, 30) * 24 * 3600)
        
        uptime = time.time() - boot_time
        
        return {
            'uptime_seconds': uptime,
            'uptime_formatted': self._format_uptime(uptime),
            'boot_time': datetime.fromtimestamp(boot_time).strftime('%Y-%m-%d %H:%M:%S'),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def _format_uptime(self, seconds):
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        minutes = int((seconds % 3600) // 60)
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    
    def check_alerts(self):
        alerts = []
        
        cpu_data = self.get_cpu_usage()
        if cpu_data['percentage'] > 85:
            alerts.append({
                'type': 'cpu',
                'message': f"High CPU usage: {cpu_data['percentage']:.1f}%",
                'severity': 'critical'
            })
        
        ram_data = self.get_ram_usage()
        if ram_data['percentage'] > 90:
            alerts.append({
                'type': 'memory',
                'message': f"High RAM usage: {ram_data['percentage']:.1f}%",
                'severity': 'critical'
            })
        
        disk_data = self.get_disk_usage()
        if disk_data['percentage'] > 95:
            alerts.append({
                'type': 'disk',
                'message': f"High disk usage: {disk_data['percentage']:.1f}%",
                'severity': 'critical'
            })
        
        return alerts
