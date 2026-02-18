# 🚀 Network Monitoring Dashboard - Deployment Guide

## Quick Start Options

### Option 1: Local Production Server ⚡
```bash
# Run in production mode
python run_production.py

# Access at: http://localhost:5000
# Network access: http://YOUR_IP:5000
```

### Option 2: Docker Deployment 🐳
```bash
# Build and run with Docker
docker-compose up -d

# Access at: http://localhost:80
```

### Option 3: Cloud Deployment ☁️

#### Heroku (Free Tier)
```bash
cd deploy
chmod +x heroku.sh
./heroku.sh
```

#### Render (Free Tier)
1. Push code to GitHub
2. Connect to Render.com
3. Use `deploy/render.yaml` configuration
4. Deploy automatically

#### Vercel (Free Tier)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

#### Railway (Free Tier)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

## 🔧 Production Configuration

### Environment Variables
```bash
FLASK_ENV=production
HOST=0.0.0.0
PORT=5000
SECRET_KEY=your-production-secret-key
```

### Security Settings
- Change default admin password
- Use HTTPS in production
- Set up firewall rules
- Enable SSL certificates

### Performance Optimization
- Use Nginx reverse proxy
- Enable Gzip compression
- Set up caching headers
- Monitor resource usage

## 🌐 Access Methods

### Local Network
```bash
# Find your IP
ipconfig  # Windows
ifconfig  # Linux/Mac

# Access from other devices
http://YOUR_IP:5000
```

### Internet Access
1. **Port Forwarding**: Forward port 5000 on your router
2. **Dynamic DNS**: Use services like No-IP or DuckDNS
3. **Cloud Hosting**: Deploy to Heroku, Render, or Vercel

## 📱 Mobile Access

### Responsive Design
- Works on all mobile devices
- Touch-friendly interface
- Optimized charts and tables

### PWA Features
- Install as mobile app
- Offline support (basic)
- Push notifications

## 🔍 Monitoring & Maintenance

### Health Checks
```bash
# Application health
curl http://localhost:5000/

# Docker health
docker-compose ps
```

### Logs
```bash
# Application logs
tail -f logs/app.log

# Docker logs
docker-compose logs -f
```

### Backup
```bash
# Database backup
cp database.db backup/database_$(date +%Y%m%d).db

# Full backup
tar -czf backup_$(date +%Y%m%d).tar.gz .
```

## 🚨 Troubleshooting

### Common Issues
1. **Port already in use**: Change port number
2. **Firewall blocking**: Allow port 5000
3. **Permission denied**: Run as administrator
4. **Dependencies missing**: Install requirements.txt

### Performance Issues
1. **High CPU**: Check system processes
2. **Memory usage**: Restart application
3. **Slow loading**: Check network connection

## 📞 Support

### Documentation
- Check `README.md` for features
- Review `API.md` for endpoints
- See `TROUBLESHOOTING.md` for issues

### Community
- GitHub Issues: Report bugs
- Discord: Live chat support
- Email: support@example.com

---

## 🎯 Quick Deployment Commands

```bash
# Fastest - Local Production
python run_production.py

# Professional - Docker
docker-compose up -d

# Cloud - Heroku
cd deploy && ./heroku.sh

# Enterprise - Custom Server
# 1. Setup Ubuntu/CentOS server
# 2. Install Docker
# 3. Run docker-compose
# 4. Configure domain and SSL
```

Choose the option that best fits your needs! 🚀
