#!/bin/bash

# Heroku Deployment Script for Network Monitoring Dashboard

echo "🚀 Deploying Network Monitoring Dashboard to Heroku..."

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install it first:"
    echo "   npm install -g heroku"
    exit 1
fi

# Login to Heroku (if not already logged in)
echo "📝 Checking Heroku authentication..."
heroku auth:whoami || {
    echo "🔐 Please login to Heroku:"
    heroku login
}

# Create Heroku app
APP_NAME="network-monitor-$(date +%s)"
echo "🏗️  Creating Heroku app: $APP_NAME"
heroku create $APP_NAME

# Set environment variables
echo "⚙️  Setting environment variables..."
heroku config:set FLASK_ENV=production --app $APP_NAME
heroku config:set HOST=0.0.0.0 --app $APP_NAME
heroku config:set PORT=5000 --app $APP_NAME

# Add buildpack
echo "📦 Adding Python buildpack..."
heroku buildpacks:set heroku/python --app $APP_NAME

# Deploy to Heroku
echo "🚀 Deploying application..."
git init
git add .
git commit -m "Deploy Network Monitoring Dashboard"
heroku git:remote -a $APP_NAME
git push heroku master

# Open the deployed app
echo "🌐 Opening deployed application..."
heroku open --app $APP_NAME

echo "✅ Deployment complete!"
echo "📊 Your Network Monitoring Dashboard is live at:"
heroku info --app $APP_NAME | grep "Web URL"
