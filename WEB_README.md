# LinkedIn Voice Assistant - Web Interface 🎤🌐

A beautiful web interface for voice-controlled LinkedIn automation using OpenAGI's TaskerAgent model.

## 🌟 Features

- **🎤 Browser Voice Input**: Speak naturally into your browser's microphone
- **🤖 OpenAGI Integration**: Uses LUX-Actor-1 model for intelligent automation
- **📊 Automatic Tracking**: Records all outreach in CSV spreadsheet
- **🎨 Modern UI**: Beautiful, responsive web interface
- **⚡ Real-time Feedback**: See your command transcribed instantly
- **📝 Smart Parsing**: Automatically extracts company, position, and count

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Activate virtual environment
source .venv/bin/activate

# Install Python packages
pip install -r requirements.txt
```

### 2. Set OpenAGI API Key

```bash
export OAGI_API_KEY=sk-your-api-key-here
```

### 3. Run the Web Server

```bash
python web_app.py
```

### 4. Open Your Browser

Navigate to: **http://localhost:5000**

## 🎯 How to Use

### Step 1: Click the Microphone
Click the purple microphone button and allow browser microphone access when prompted.

### Step 2: Speak Your Command
Say something like:
> "Reach out to 10 people from Google about the Software Engineer position"

The system will automatically:
- Convert your speech to text
- Parse company name, position, and number of people
- Display the extracted information

### Step 3: Confirm Details
Review the auto-filled form and make any adjustments needed.

### Step 4: Execute
Click "Execute Automation" and watch the magic happen!

## 🗣️ Voice Command Examples

- "Contact 15 people at Microsoft regarding the Product Manager role"
- "Reach out to 5 people from Amazon about the Data Scientist position"
- "Send connection requests to 20 people at Tesla for the Software Engineer position"

## 🏗️ Architecture

### Frontend (`templates/index.html`)
- **Web Speech API**: Browser-native voice recognition
- **Responsive Design**: Works on desktop and tablet
- **Real-time Updates**: Live status and transcript display
- **Smart Parsing**: Extracts key information from voice input

### Backend (`web_app.py`)
- **Flask Server**: Lightweight Python web server
- **OpenAGI Integration**: Uses TaskerAgent for automation
- **Async Execution**: Non-blocking automation
- **Result Tracking**: Saves to CSV and HTML reports

### Automation Flow

```
Voice Input → Speech-to-Text → Parse Command → Confirm Details
     ↓
TaskerAgent → LinkedIn Automation → Connection Requests
     ↓
Save to Spreadsheet → Generate HTML Report → Show Results
```

## 📋 Detailed Workflow

### What the Automation Does

1. **Opens LinkedIn** in your browser
2. **Searches** for people at the target company
3. **Filters** to show only people results
4. **Iterates** through search results
5. For each person:
   - Clicks "Connect" (or "More" → "Connect")
   - Clicks "Add a note"
   - Types personalized message mentioning:
     - Company name
     - Position you're applying for
     - Request for conversation
   - Sends the connection request
   - Records their name and title
6. **Tracks** all contacts in spreadsheet
7. **Generates** HTML execution report

### The Personalized Message Template

```
Hi [Name],

I hope this message finds you well. I came across your profile 
while researching [Company], and I'm really impressed by the work 
you and the team are doing.

I'm currently exploring the [Position] position at [Company] and 
would love to connect for a brief conversation to learn more about 
the role and the team culture.

Would you be open to a quick chat at your convenience?

Best regards
```

## 🛠️ Technical Details

### OpenAGI TaskerAgent Configuration

```python
TaskerAgent(
    model="lux-actor-1",        # OpenAGI's automation model
    max_steps=30,               # Maximum automation steps
    temperature=0.0,            # Deterministic execution
    step_observer=observer      # Tracks execution
)
```

### Todos Breakdown

The automation is broken into specific, actionable steps (todos) that the LUX model executes sequentially:

1. Navigate to LinkedIn
2. Search for company
3. Apply people filter
4. Loop through results
5. For each person: connect + add note + send
6. Track and report

### Action Handler & Image Provider

```python
AsyncScreenshotMaker()          # Captures screen for the model
AsyncPyautoguiActionHandler()   # Controls mouse/keyboard
```

## 📊 Output Files

### CSV Tracking (`linkedin_outreach.csv`)
Columns:
- Timestamp
- Company Name
- Position Applied
- Contact Name
- Contact Title
- Connection Status
- Message Sent
- Response Status
- Notes

### HTML Report (`results/linkedin/linkedin_execution_*.html`)
- Screenshot thumbnails of each step
- Tool calls and responses
- Timestamps
- Success/failure indicators
- Full execution history

## 🔧 Configuration

### Modify Number of Steps
Edit `web_app.py`:
```python
self.max_steps = 30  # Increase for longer workflows
```

### Change Model
```python
self.model = "lux-actor-1"  # Use different OpenAGI model
```

### Customize Message Template
Edit the message in the todos list within `web_app.py`:
```python
f"Type a personalized message: 'Your custom message here...'"
```

## 🎨 UI Customization

The web interface uses modern CSS with:
- Purple gradient theme
- Pulsing animation on recording
- Responsive design
- Clean typography
- Smooth transitions

To customize colors, edit `templates/index.html`:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

## 🔒 Browser Permissions

The app requires:
- ✅ **Microphone access** for voice input
- ✅ **Screen recording** (for PyAutoGUI on macOS)
- ✅ **Accessibility** (for PyAutoGUI on macOS)

Grant these in **System Preferences → Security & Privacy**

## 🐛 Troubleshooting

### Voice Recognition Not Working
- **Chrome/Edge**: Best support for Web Speech API
- **Safari**: Limited support
- **Firefox**: May require flags

### "Microphone not found"
1. Check browser permissions
2. Ensure microphone is connected
3. Try different browser

### Automation Stops Midway
- LinkedIn may have rate limits
- Increase `max_steps` in configuration
- Check HTML report for error details

### "OAGI_API_KEY not found"
```bash
export OAGI_API_KEY=your_key_here
```

## 📈 Best Practices

### LinkedIn Limits
- **Daily limit**: ~100 connection requests
- **Weekly limit**: ~200-300 connection requests
- Start with small batches (5-10 people)
- Space out your automation runs

### Message Personalization
- Always send a note (never skip)
- Mention specific role or team
- Be genuine and professional
- Keep it concise

### Testing
1. Test with 1-2 people first
2. Verify messages are sending correctly
3. Check LinkedIn for confirmation
4. Review CSV and HTML reports

## 🔄 Comparison: CLI vs Web Interface

### CLI Version (`voice_linkedin_assistant.py`)
- ✅ Desktop voice recognition
- ✅ Text-to-speech feedback
- ✅ Terminal-based
- ❌ Requires microphone setup

### Web Version (`web_app.py` + `templates/index.html`)
- ✅ Browser-based voice input
- ✅ Beautiful visual interface
- ✅ Works on any device
- ✅ No local voice setup needed
- ✅ Real-time visual feedback

## 🚦 API Endpoints

### `GET /`
Serves the web interface

### `POST /api/execute`
Execute LinkedIn automation
```json
{
  "command": "voice command text",
  "company": "Google",
  "position": "Software Engineer",
  "num_people": 10
}
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully completed LinkedIn outreach",
  "data": {
    "completed": 10,
    "company": "Google",
    "position": "Software Engineer"
  }
}
```

### `GET /api/status`
Check server status
```json
{
  "status": "online",
  "api_key_configured": true,
  "timestamp": "2025-12-16T10:30:00"
}
```

## 📚 Learn More

### OpenAGI Documentation
- [TaskerAgent Guide](https://docs.openagi.com/tasker-agent)
- [LUX Model Overview](https://docs.openagi.com/models/lux)
- [Desktop Automation](https://docs.openagi.com/automation)

### Similar Examples
- **CVS Appointment Booking**: Multi-step form automation
- **Amazon Data Crawling**: Web scraping with OpenAGI
- **Nike Shopping**: E-commerce automation

## 🎓 How It Works (Technical Deep Dive)

### 1. Voice Capture (Browser)
```javascript
const SpeechRecognition = window.webkitSpeechRecognition;
recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    // Send to backend for processing
}
```

### 2. Command Parsing (Backend)
```python
# Extract company, position, number from natural language
company = parse_company(transcript)
position = parse_position(transcript)
num_people = parse_number(transcript)
```

### 3. TaskerAgent Execution
```python
tasker = TaskerAgent(model="lux-actor-1")
tasker.set_task(instruction, todos)
await tasker.execute(action_handler, image_provider)
```

### 4. Automation Loop
```
FOR each person in search results:
    1. Screenshot → LUX model analyzes
    2. Model decides action (click, type, wait)
    3. PyAutoGUI executes action
    4. Repeat until todo complete
```

### 5. Result Tracking
```python
tracker.add_multiple_records(contacts)
observer.export("html", report_file)
```

## 🎬 Demo Video Ideas

1. **Opening**: Show web interface
2. **Voice Command**: Click mic and speak
3. **Parsing**: Show auto-filled form
4. **Execution**: Watch browser automate
5. **Results**: Show CSV and HTML report

## 🤝 Contributing

Ideas for enhancements:
- [ ] Multi-language support
- [ ] Custom message templates UI
- [ ] Response tracking dashboard
- [ ] Email notifications
- [ ] InMail automation
- [ ] Follow-up message scheduling

## ⚠️ Disclaimer

- Use responsibly and ethically
- Comply with LinkedIn Terms of Service
- Don't spam people
- Personalize your messages
- Respect rate limits
- Be genuine in your outreach

## 📄 License

MIT License - Use freely for your job search!

---

**Built with ❤️ using OpenAGI and modern web technologies**

**Good luck with your networking! 🚀**
