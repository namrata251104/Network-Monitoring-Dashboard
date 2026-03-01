import streamlit as st
import psutil
import time
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pandas as pd
import random

# Page configuration
st.set_page_config(
    page_title="Network Monitoring Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 1rem;
        opacity: 0.8;
    }
    .alert-success {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .alert-warning {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .alert-danger {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Authentication
def authenticate():
    """Simple authentication"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.title("🔐 Network Monitor Login")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            username_input = st.text_input("Username", key="login_username")
            password_input = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login", use_container_width=True):
                if username_input == "admin" and password_input == "admin123":
                    st.session_state.authenticated = True
                    st.session_state.user_name = username_input  # Use different key
                    st.success("Login successful! Redirecting...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        
        return False
    return True

# Get system metrics
def get_system_metrics():
    """Get real-time system metrics"""
    try:
        # CPU metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_freq = psutil.cpu_freq()
        cpu_cores = psutil.cpu_count()
        
        # Memory metrics
        memory = psutil.virtual_memory()
        
        # Disk metrics
        disk = psutil.disk_usage('/')
        
        # Network metrics
        network = psutil.net_io_counters()
        
        # Process information
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort by CPU usage and get top 10
        processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        top_processes = processes[:10]
        
        return {
            'cpu': {
                'percent': cpu_percent,
                'frequency': cpu_freq.current if cpu_freq else 0,
                'cores': cpu_cores
            },
            'memory': {
                'percent': memory.percent,
                'used': memory.used / (1024**3),  # GB
                'total': memory.total / (1024**3)  # GB
            },
            'disk': {
                'percent': disk.percent,
                'used': disk.used / (1024**3),  # GB
                'total': disk.total / (1024**3)  # GB
            },
            'network': {
                'bytes_sent': network.bytes_sent / (1024**2),  # MB
                'bytes_recv': network.bytes_recv / (1024**2),  # MB
                'packets_sent': network.packets_sent,
                'packets_recv': network.packets_recv
            },
            'processes': top_processes,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        st.error(f"Error getting system metrics: {e}")
        return None

# Check for alerts
def check_alerts(metrics):
    """Check for system alerts"""
    alerts = []
    
    if metrics:
        if metrics['cpu']['percent'] > 80:
            alerts.append({
                'type': 'CPU',
                'severity': 'danger',
                'message': f"High CPU usage: {metrics['cpu']['percent']:.1f}%"
            })
        elif metrics['cpu']['percent'] > 60:
            alerts.append({
                'type': 'CPU',
                'severity': 'warning',
                'message': f"Moderate CPU usage: {metrics['cpu']['percent']:.1f}%"
            })
        
        if metrics['memory']['percent'] > 85:
            alerts.append({
                'type': 'Memory',
                'severity': 'danger',
                'message': f"High memory usage: {metrics['memory']['percent']:.1f}%"
            })
        elif metrics['memory']['percent'] > 70:
            alerts.append({
                'type': 'Memory',
                'severity': 'warning',
                'message': f"Moderate memory usage: {metrics['memory']['percent']:.1f}%"
            })
        
        if metrics['disk']['percent'] > 90:
            alerts.append({
                'type': 'Disk',
                'severity': 'danger',
                'message': f"Low disk space: {metrics['disk']['percent']:.1f}% used"
            })
        elif metrics['disk']['percent'] > 80:
            alerts.append({
                'type': 'Disk',
                'severity': 'warning',
                'message': f"Disk space getting low: {metrics['disk']['percent']:.1f}% used"
            })
    
    return alerts

# Main dashboard
def main_dashboard():
    """Main dashboard function"""
    st.markdown('<h1 class="main-header">📊 Network Monitoring Dashboard</h1>', unsafe_allow_html=True)
    
    # Auto-refresh option
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        auto_refresh = st.checkbox("🔄 Auto-refresh (5 seconds)", value=True)
    
    # Get metrics
    metrics = get_system_metrics()
    
    if metrics:
        # Display last update time
        st.info(f"📅 Last updated: {metrics['timestamp']}")
        
        # Alert section
        alerts = check_alerts(metrics)
        if alerts:
            st.markdown("### 🚨 System Alerts")
            for alert in alerts:
                if alert['severity'] == 'danger':
                    st.markdown(f'<div class="alert-danger"><strong>{alert["type"]} Alert:</strong> {alert["message"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="alert-warning"><strong>{alert["type"]} Warning:</strong> {alert["message"]}</div>', unsafe_allow_html=True)
        
        # Metrics cards
        st.markdown("### 📈 System Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">CPU Usage</div>
                <div class="metric-value">{metrics['cpu']['percent']:.1f}%</div>
                <div class="metric-label">{metrics['cpu']['cores']} cores</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Memory Usage</div>
                <div class="metric-value">{metrics['memory']['percent']:.1f}%</div>
                <div class="metric-label">{metrics['memory']['used']:.1f} GB / {metrics['memory']['total']:.1f} GB</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Disk Usage</div>
                <div class="metric-value">{metrics['disk']['percent']:.1f}%</div>
                <div class="metric-label">{metrics['disk']['used']:.1f} GB / {metrics['disk']['total']:.1f} GB</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Network</div>
                <div class="metric-value">{metrics['network']['bytes_sent']:.1f} MB</div>
                <div class="metric-label">Sent / {metrics['network']['bytes_recv']:.1f} MB Recv</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Charts section
        st.markdown("### 📊 Performance Charts")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # CPU and Memory chart
            fig_cpu_mem = go.Figure()
            fig_cpu_mem.add_trace(go.Bar(
                name='CPU Usage',
                x=['CPU'],
                y=[metrics['cpu']['percent']],
                marker_color='rgb(55, 83, 109)'
            ))
            fig_cpu_mem.add_trace(go.Bar(
                name='Memory Usage',
                x=['Memory'],
                y=[metrics['memory']['percent']],
                marker_color='rgb(26, 118, 255)'
            ))
            fig_cpu_mem.update_layout(
                title='CPU & Memory Usage',
                yaxis_title='Percentage (%)',
                height=300
            )
            st.plotly_chart(fig_cpu_mem, use_container_width=True)
        
        with col2:
            # Disk usage chart
            fig_disk = go.Figure(data=[go.Pie(
                labels=['Used', 'Free'],
                values=[metrics['disk']['percent'], 100 - metrics['disk']['percent']],
                hole=0.3,
                marker_colors=['rgb(255, 99, 132)', 'rgb(75, 192, 192)']
            )])
            fig_disk.update_layout(
                title='Disk Usage',
                height=300
            )
            st.plotly_chart(fig_disk, use_container_width=True)
        
        # Top processes
        st.markdown("### 🔄 Top Processes")
        
        if metrics['processes']:
            process_data = []
            for proc in metrics['processes'][:10]:
                process_data.append({
                    'PID': proc['pid'],
                    'Name': proc['name'],
                    'CPU %': proc['cpu_percent'],
                    'Memory %': proc['memory_percent']
                })
            
            df_processes = pd.DataFrame(process_data)
            st.dataframe(df_processes, use_container_width=True)
        else:
            st.warning("No process data available")
        
        # Auto-refresh
        if auto_refresh:
            time.sleep(5)
            st.rerun()

# Logs page
def logs_page():
    """System logs page"""
    st.markdown('<h1 class="main-header">📜 System Logs</h1>', unsafe_allow_html=True)
    
    # Generate sample log data
    import random
    from datetime import datetime, timedelta
    
    log_levels = ['INFO', 'WARNING', 'ERROR', 'DEBUG']
    log_sources = ['System', 'Network', 'CPU', 'Memory', 'Disk', 'Security']
    
    # Generate sample logs
    logs = []
    for i in range(50):
        timestamp = datetime.now() - timedelta(minutes=random.randint(0, 1440))
        level = random.choice(log_levels)
        source = random.choice(log_sources)
        
        if level == 'INFO':
            messages = [
                f"{source} monitoring started successfully",
                f"{source} metrics collected",
                f"{source} status check completed",
                f"{source} performance within normal range"
            ]
        elif level == 'WARNING':
            messages = [
                f"{source} usage above threshold",
                f"{source} response time increased",
                f"{source} connection timeout",
                f"{source} resource utilization high"
            ]
        elif level == 'ERROR':
            messages = [
                f"{source} connection failed",
                f"{source} service unavailable",
                f"{source} critical error occurred",
                f"{source} operation failed"
            ]
        else:  # DEBUG
            messages = [
                f"{source} debug information",
                f"{source} configuration loaded",
                f"{source} module initialized",
                f"{source} cache cleared"
            ]
        
        logs.append({
            'timestamp': timestamp,
            'level': level,
            'source': source,
            'message': random.choice(messages)
        })
    
    # Sort logs by timestamp
    logs.sort(key=lambda x: x['timestamp'], reverse=True)
    
    # Filters
    st.markdown("### 🔍 Filter Logs")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        selected_level = st.selectbox("Log Level", ["All"] + log_levels)
    with col2:
        selected_source = st.selectbox("Source", ["All"] + log_sources)
    with col3:
        time_range = st.selectbox("Time Range", ["Last Hour", "Last 24 Hours", "Last Week", "All"])
    with col4:
        search_term = st.text_input("Search")
    
    # Apply filters
    filtered_logs = logs.copy()
    
    if selected_level != "All":
        filtered_logs = [log for log in filtered_logs if log['level'] == selected_level]
    
    if selected_source != "All":
        filtered_logs = [log for log in filtered_logs if log['source'] == selected_source]
    
    if search_term:
        filtered_logs = [log for log in filtered_logs if search_term.lower() in log['message'].lower()]
    
    # Log statistics
    st.markdown("### 📊 Log Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_logs = len(filtered_logs)
        st.metric("Total Logs", total_logs)
    
    with col2:
        error_count = len([log for log in filtered_logs if log['level'] == 'ERROR'])
        st.metric("Errors", error_count)
    
    with col3:
        warning_count = len([log for log in filtered_logs if log['level'] == 'WARNING'])
        st.metric("Warnings", warning_count)
    
    with col4:
        info_count = len([log for log in filtered_logs if log['level'] == 'INFO'])
        st.metric("Info", info_count)
    
    # Log level distribution chart
    if filtered_logs:
        level_counts = {}
        for log in filtered_logs:
            level_counts[log['level']] = level_counts.get(log['level'], 0) + 1
        
        fig_levels = go.Figure(data=[
            go.Bar(x=list(level_counts.keys()), y=list(level_counts.values()))
        ])
        fig_levels.update_layout(
            title="Log Level Distribution",
            xaxis_title="Log Level",
            yaxis_title="Count",
            height=300
        )
        st.plotly_chart(fig_levels, use_container_width=True)
    
    # Logs table
    st.markdown("### 📋 Log Entries")
    
    if filtered_logs:
        # Create DataFrame for display
        df_logs = pd.DataFrame(filtered_logs)
        df_logs['timestamp'] = df_logs['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Color code log levels
        def color_log_level(level):
            if level == 'ERROR':
                return 'background-color: #ffebee; color: #c62828'
            elif level == 'WARNING':
                return 'background-color: #fff3e0; color: #ef6c00'
            elif level == 'INFO':
                return 'background-color: #e8f5e8; color: #2e7d32'
            else:  # DEBUG
                return 'background-color: #f3e5f5; color: #7b1fa2'
        
        # Apply styling
        styled_df = df_logs.style.applymap(
            lambda x: color_log_level(x) if x in ['ERROR', 'WARNING', 'INFO', 'DEBUG'] else '',
            subset=['level']
        )
        
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
    else:
        st.warning("No logs found matching the selected filters.")
    
    # Export functionality
    st.markdown("### 💾 Export Logs")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export as CSV", use_container_width=True):
            if filtered_logs:
                csv_df = pd.DataFrame(filtered_logs)
                csv_df['timestamp'] = csv_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
                csv = csv_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"system_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No logs to export")
    
    with col2:
        if st.button("🗑️ Clear Logs", use_container_width=True):
            st.success("Logs cleared successfully!")
            time.sleep(1)
            st.rerun()

# Settings page
def settings_page():
    """Settings configuration page"""
    st.markdown('<h1 class="main-header">⚙️ Settings</h1>', unsafe_allow_html=True)
    
    st.markdown("### 🔔 Alert Thresholds")
    
    col1, col2 = st.columns(2)
    
    with col1:
        cpu_threshold = st.slider("CPU Alert Threshold (%)", 50, 95, 80)
        memory_threshold = st.slider("Memory Alert Threshold (%)", 60, 95, 85)
    
    with col2:
        disk_threshold = st.slider("Disk Alert Threshold (%)", 70, 95, 90)
        refresh_interval = st.slider("Refresh Interval (seconds)", 1, 30, 5)
    
    st.markdown("### 🎨 Display Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        show_alerts = st.checkbox("Show Alerts", value=True)
        show_charts = st.checkbox("Show Charts", value=True)
    
    with col2:
        show_processes = st.checkbox("Show Processes", value=True)
        dark_mode = st.checkbox("Dark Mode", value=False)
    
    if st.button("💾 Save Settings", use_container_width=True):
        st.success("Settings saved successfully!")
        time.sleep(1)
        st.rerun()

# Main app
def main():
    """Main application"""
    # Authentication
    if not authenticate():
        return
    
    # Sidebar navigation
    st.sidebar.markdown(f"### 👋 Welcome, {st.session_state.user_name}!")
    
    if st.sidebar.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.user_name = None
        st.rerun()
    
    page = st.sidebar.selectbox("📍 Navigate", ["📊 Dashboard", "📜 Logs", "⚙️ Settings"])
    
    if page == "📊 Dashboard":
        main_dashboard()
    elif page == "📜 Logs":
        logs_page()
    elif page == "⚙️ Settings":
        settings_page()

if __name__ == "__main__":
    main()
