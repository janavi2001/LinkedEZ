#!/bin/bash

# Setup script for LinkedIn Voice Assistant

echo "🚀 Setting up LinkedIn Voice Assistant..."
echo ""

# Check Python version
echo "📋 Checking Python version..."
python3 --version

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Check if portaudio is installed (required for PyAudio)
echo "🎤 Checking for portaudio..."
if ! brew list portaudio &>/dev/null; then
    echo "📦 Installing portaudio via Homebrew..."
    brew install portaudio
else
    echo "✅ portaudio is already installed"
fi

# Install Python packages
echo "📚 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check for OpenAGI API key
echo ""
echo "🔑 Checking for OpenAGI API key..."
if [ -z "$OAGI_API_KEY" ]; then
    echo "⚠️  OAGI_API_KEY not found in environment"
    echo "💡 Please set your API key:"
    echo "   export OAGI_API_KEY=your_api_key_here"
    echo ""
    echo "   Or add it to a .env file:"
    echo "   echo 'OAGI_API_KEY=your_api_key_here' > .env"
else
    echo "✅ OAGI_API_KEY is set"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo "📝 Creating .gitignore..."
    cat > .gitignore << EOL
# Virtual environment
.venv/
venv/
env/

# API keys and credentials
.env
credentials.json

# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# Data files
*.csv
*.xlsx

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOL
    echo "✅ Created .gitignore"
else
    echo "✅ .gitignore already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "   1. Make sure you're logged into LinkedIn in your browser"
echo "   2. Set your OpenAGI API key (if not already set)"
echo "   3. Run the assistant:"
echo "      python voice_linkedin_assistant.py"
echo ""
echo "📖 For more information, see README.md"
