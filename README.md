# Network Monitoring Web Dashboard

A professional, production-ready web dashboard for monitoring system/server metrics with real-time updates, beautiful UI, and comprehensive alert system.

## 🚀 Features

### Core Functionality
- **Real-time System Monitoring**: CPU, RAM, Disk, Network metrics
- **Live Data Updates**: Auto-refresh every 2 seconds
- **Smart Data Fallback**: Uses real system data when available, simulated data otherwise
- **Professional UI**: Modern glass-morphism design with smooth animations
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile

### Authentication & Security
- **Secure Login System**: Session-based authentication with bcrypt password hashing
- **Admin Dashboard**: Default admin credentials (admin/admin123)
- **Login Logging**: Tracks all login attempts with IP and user agent
- **Session Management**: Secure session handling with automatic timeout

### Monitoring Features
- **CPU Monitoring**: Usage percentage, cores, frequency, load average
- **RAM Monitoring**: Total, used, available memory with swap information
- **Disk Monitoring**: Usage percentage, read/write statistics
- **Network Activity**: Upload/download speeds, connection count
- **Process Monitoring**: Top 10 processes by CPU usage
- **System Information**: Uptime, boot time, system status

### Alert System
- **Threshold Monitoring**: Configurable alerts for CPU > 85%, RAM > 90%, Disk > 95%
- **Real-time Notifications**: Browser notifications for critical alerts
- **Alert History**: Track and manage all system alerts
- **Visual Indicators**: Color-coded alert banners and badges

### Advanced Features
- **Dark Mode**: Toggle between light and dark themes
- **Customizable Settings**: Configure thresholds, refresh intervals, themes
- **Performance Charts**: Historical data visualization with Chart.js
- **Toast Notifications**: Non-intrusive feedback system
- **Loading Animations**: Professional loading states and transitions
- **Keyboard Shortcuts**: Ctrl+R (refresh), Ctrl+D (dark mode), Esc (close sidebar)

## 🛠 Tech Stack

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: Database ORM
- **psutil**: System monitoring library
- **bcrypt**: Password hashing
- **SQLite**: Database storage

### Frontend
- **HTML5/CSS3**: Modern markup and styling
- **JavaScript ES6+**: Interactive functionality
- **Bootstrap 5**: UI framework
- **Chart.js**: Data visualization
- **FontAwesome**: Icon library
- **Inter Font**: Professional typography

## 📁 Project Structure

```
network-monitoring-dashboard/
├── app.py                     # Main Flask application
├── requirements.txt           # Python dependencies
├── database.db              # SQLite database (auto-created)
├── templates/               # HTML templates
│   ├── base.html           # Base template with layout
│   ├── login.html          # Login page
│   ├── dashboard.html      # Main dashboard
│   ├── settings.html       # Settings page
│   ├── logs.html          # System logs page
│   ├── 404.html           # 404 error page
│   └── 500.html           # 500 error page
├── static/                 # Static assets
│   ├── css/
│   │   └── dashboard.css  # Main stylesheet
│   ├── js/
│   │   └── dashboard.js   # Main JavaScript file
│   └── images/           # Image assets
├── routes/                # Flask route modules
│   ├── auth.py           # Authentication routes
│   ├── api.py            # API endpoints
│   └── main.py           # Main page routes
├── models/               # Database models
│   └── database.py       # SQLAlchemy models
└── utils/               # Utility modules
    └── system_monitor.py # System monitoring logic
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone/Download the Project
```bash
# If using git
git clone <repository-url>
cd network-monitoring-dashboard

# Or download and extract the ZIP file
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python app.py
```

### Step 5: Access the Dashboard
Open your web browser and navigate to:
```
http://localhost:5000
```

### Default Login Credentials
- **Username**: admin
- **Password**: admin123

## 📊 API Endpoints

### System Metrics
- `GET /api/cpu` - CPU usage information
- `GET /api/ram` - RAM usage information
- `GET /api/disk` - Disk usage information
- `GET /api/network` - Network activity data
- `GET /api/processes` - Top processes by CPU usage
- `GET /api/system-info` - System information (uptime, boot time)

### Alerts & Management
- `GET /api/alerts` - Current system alerts
- `POST /api/resolve-alert/<id>` - Resolve an alert
- `GET /api/all-metrics` - All metrics in single request
- `GET /api/historical-data` - Historical performance data

### Authentication
- `POST /auth/login` - User login
- `GET /auth/logout` - User logout
- `GET /auth/check-session` - Check session status

## ⚙️ Configuration

### Environment Variables
Create a `.env` file in the root directory:
```env
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
DATABASE_URL=sqlite:///database.db
```

### Customizable Settings
- **Alert Thresholds**: CPU, RAM, Disk usage percentages
- **Refresh Intervals**: Auto-refresh frequency (1-30 seconds)
- **Themes**: Light, dark, green, purple color schemes
- **Notifications**: Browser notifications and sounds
- **Chart Types**: Line, bar, doughnut chart options

## 🔧 Customization

### Adding New Metrics
1. Update `utils/system_monitor.py` with new monitoring functions
2. Add corresponding API endpoints in `routes/api.py`
3. Update frontend templates and JavaScript to display new data

### Custom Themes
Modify CSS variables in `static/css/dashboard.css`:
```css
:root {
    --primary-color: #your-color;
    --secondary-color: #your-secondary-color;
    /* Add more custom colors */
}
```

### Database Schema
Models are defined in `models/database.py`. Add new models or extend existing ones as needed.

## 🚨 Troubleshooting

### Common Issues

**1. Port Already in Use**
```bash
# Error: Address already in use
# Solution: Kill existing process or change port
python app.py --port 5001
```

**2. Permission Denied (System Monitoring)**
- The application automatically falls back to simulated data
- No action required - all features work with simulated data

**3. Database Issues**
```bash
# Delete and recreate database
rm database.db
python app.py  # Database will be recreated automatically
```

**4. CSS/JS Not Loading**
- Ensure static files are in correct directories
- Check file paths in templates
- Verify Flask static file serving is working

### Performance Optimization
- Enable production mode with `FLASK_ENV=production`
- Use Gunicorn or uWSGI for production deployment
- Configure reverse proxy (Nginx) for better performance
- Implement database connection pooling

## 📱 Mobile Support

The dashboard is fully responsive and works on:
- Desktop browsers (Chrome, Firefox, Safari, Edge)
- Tablet devices (iPad, Android tablets)
- Mobile phones (iOS, Android)

### Mobile Features
- Collapsible sidebar navigation
- Touch-friendly interface
- Optimized charts for small screens
- Responsive metric cards

## 🔒 Security Considerations

### Production Deployment
1. Change default admin password
2. Use strong SECRET_KEY
3. Enable HTTPS
4. Implement rate limiting
5. Add CSRF protection
6. Use environment variables for sensitive data

### Recommended Security Headers
```python
# Add to app.py for production
@app.after_request
def security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
```

## 📈 Performance Metrics

The dashboard displays:
- **CPU Usage**: Real-time percentage with core information
- **Memory Usage**: RAM and swap utilization
- **Disk Usage**: Storage capacity and I/O statistics
- **Network Activity**: Bandwidth usage and connection count
- **Process List**: Top resource-consuming processes
- **System Uptime**: How long the system has been running

## 🎨 UI Features

### Visual Design
- **Glass Morphism**: Modern frosted glass effects
- **Gradient Backgrounds**: Beautiful color transitions
- **Smooth Animations**: CSS transitions and JavaScript animations
- **Hover Effects**: Interactive feedback on all clickable elements
- **Loading States**: Professional loading animations

### User Experience
- **Intuitive Navigation**: Sidebar menu with icons
- **Quick Actions**: Refresh, dark mode, notifications
- **Real-time Updates**: Live data without page refresh
- **Toast Notifications**: Non-intrusive feedback messages
- **Responsive Layout**: Adapts to any screen size

## 🔄 Data Flow

1. **Frontend Request**: JavaScript calls API endpoints
2. **Backend Processing**: Flask routes handle requests
3. **System Monitoring**: psutil gathers real system data
4. **Data Processing**: Format and validate metrics
5. **Response**: JSON data returned to frontend
6. **UI Update**: JavaScript updates charts and displays

## 📝 Logging & Monitoring

### Application Logs
- Login attempts (successful/failed)
- System alerts and resolutions
- Error messages and exceptions
- Performance metrics

### Database Tables
- `users`: User accounts and credentials
- `login_logs`: Authentication history
- `alerts`: System alert records

## 🚀 Deployment Options

### Development
```bash
python app.py
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Examine the code comments
4. Create an issue with detailed information

## 🎯 Future Enhancements

- Multi-server monitoring
- Historical data analytics
- Email/SMS notifications
- Custom dashboard widgets
- API authentication tokens
- Performance optimization
- Mobile app companion
- Integration with monitoring services

---

**Built with ❤️ for professional system monitoring**
