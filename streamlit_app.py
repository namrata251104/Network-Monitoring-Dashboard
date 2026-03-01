import streamlit as st
import psutil
import time
import pandas as pd
import random
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Network Monitoring Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
</style>
""", unsafe_allow_html=True)

# Authentication
def authenticate():
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
                    st.session_state.user_name = username_input
                    st.success("Login successful! Redirecting...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        
        return False
    return True

# Get system metrics
def get_system_metrics():
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        network = psutil.net_io_counters()
        
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        top_processes = processes[:10]
        
        return {
            'cpu': {'percent': cpu_percent, 'cores': psutil.cpu_count()},
            'memory': {
                'percent': memory.percent,
                'used': memory.used / (1024**3),
                'total': memory.total / (1024**3)
            },
            'disk': {
                'percent': disk.percent,
                'used': disk.used / (1024**3),
                'total': disk.total / (1024**3)
            },
            'network': {
                'bytes_sent': network.bytes_sent / (1024**2),
                'bytes_recv': network.bytes_recv / (1024**2)
            },
            'processes': top_processes,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        st.error(f"Error getting system metrics: {e}")
        return None

# Main dashboard
def main_dashboard():
    st.markdown('<h1 class="main-header">📊 Network Monitoring Dashboard</h1>', unsafe_allow_html=True)
    
    auto_refresh = st.checkbox("🔄 Auto-refresh (5 seconds)", value=True)
    
    metrics = get_system_metrics()
    
    if metrics:
        st.info(f"📅 Last updated: {metrics['timestamp']}")
        
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
        
        # Simple charts using Streamlit
        st.markdown("### 📊 Performance Charts")
        col1, col2 = st.columns(2)
        
        with col1:
            # CPU and Memory bar chart
            chart_data = pd.DataFrame({
                'Metric': ['CPU Usage', 'Memory Usage'],
                'Percentage': [metrics['cpu']['percent'], metrics['memory']['percent']]
            })
            st.bar_chart(chart_data.set_index('Metric'))
        
        with col2:
            # Disk usage pie chart
            disk_data = pd.DataFrame({
                'Category': ['Used', 'Free'],
                'Size': [metrics['disk']['percent'], 100 - metrics['disk']['percent']]
            })
            st.bar_chart(disk_data.set_index('Category'))
        
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
        
        # Alerts
        st.markdown("### 🚨 System Alerts")
        alerts = []
        
        if metrics['cpu']['percent'] > 80:
            alerts.append(f"⚠️ High CPU usage: {metrics['cpu']['percent']:.1f}%")
        if metrics['memory']['percent'] > 85:
            alerts.append(f"⚠️ High memory usage: {metrics['memory']['percent']:.1f}%")
        if metrics['disk']['percent'] > 90:
            alerts.append(f"⚠️ Low disk space: {metrics['disk']['percent']:.1f}% used")
        
        if alerts:
            for alert in alerts:
                st.warning(alert)
        else:
            st.success("✅ All systems operating normally")
        
        if auto_refresh:
            time.sleep(5)
            st.rerun()

# Settings page
def settings_page():
    st.markdown('<h1 class="main-header">⚙️ Settings</h1>', unsafe_allow_html=True)
    
    st.markdown("### 🔔 Alert Thresholds")
    
    col1, col2 = st.columns(2)
    
    with col1:
        cpu_threshold = st.slider("CPU Alert Threshold (%)", 50, 95, 80)
        memory_threshold = st.slider("Memory Alert Threshold (%)", 60, 95, 85)
    
    with col2:
        disk_threshold = st.slider("Disk Alert Threshold (%)", 70, 95, 90)
        refresh_interval = st.slider("Refresh Interval (seconds)", 1, 30, 5)
    
    if st.button("💾 Save Settings", use_container_width=True):
        st.success("Settings saved successfully!")
        time.sleep(1)
        st.rerun()

# Main app
def main():
    if not authenticate():
        return
    
    st.sidebar.markdown(f"### 👋 Welcome, {st.session_state.user_name}!")
    
    if st.sidebar.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.user_name = None
        st.rerun()
    
    page = st.sidebar.selectbox("📍 Navigate", ["📊 Dashboard", "⚙️ Settings"])
    
    if page == "📊 Dashboard":
        main_dashboard()
    elif page == "⚙️ Settings":
        settings_page()

if __name__ == "__main__":
    main()
