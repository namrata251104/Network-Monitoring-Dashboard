#!/usr/bin/env python3
"""
Production server for Network Monitoring Dashboard
"""

from app import app
import os

if __name__ == '__main__':
    # Production configuration
    app.config['DEBUG'] = False
    app.config['ENV'] = 'production'
    
    # Use production server
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    
    print(f"🚀 Starting Network Monitoring Dashboard on http://{host}:{port}")
    print("📊 Dashboard is now running in production mode")
    print("🔒 Access from other devices on your network using your IP address")
    
    app.run(
        host=host,
        port=port,
        debug=False,
        threaded=True
    )
