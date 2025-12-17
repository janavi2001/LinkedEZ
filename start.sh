#!/bin/bash

# Quick Setup Script for LinkedIn Voice Assistant with ElevenLabs

echo "🚀 LinkedIn Voice Assistant Setup"
echo "=================================="
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Creating from template..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo ""
    echo "⚠️  Please edit .env and add your API keys:"
    echo "   1. OAGI_API_KEY (already set)"
    echo "   2. ELEVENLABS_API_KEY (get from https://elevenlabs.io)"
    echo ""
    exit 1
fi

# Load environment variables
source .env

# Check OAGI API key
if [ -z "$OAGI_API_KEY" ]; then
    echo "❌ OAGI_API_KEY not set in .env"
    exit 1
else
    echo "✅ OAGI_API_KEY configured"
fi

# Check ElevenLabs API key
if [ -z "$ELEVENLABS_API_KEY" ] || [ "$ELEVENLABS_API_KEY" = "your-elevenlabs-api-key-here" ]; then
    echo "⚠️  ELEVENLABS_API_KEY not set!"
    echo ""
    echo "📝 To get your ElevenLabs API key:"
    echo "   1. Go to https://elevenlabs.io/app/speech-synthesis"
    echo "   2. Sign up for a free account"
    echo "   3. Navigate to Settings → API Keys"
    echo "   4. Copy your API key"
    echo "   5. Edit .env and replace 'your-elevenlabs-api-key-here'"
    echo ""
    exit 1
else
    echo "✅ ELEVENLABS_API_KEY configured"
fi

echo ""
echo "✅ All API keys configured!"
echo ""
echo "🌐 Starting web server..."
echo "   Access at: http://localhost:5000"
echo ""

# Start the web app
python web_app.py
