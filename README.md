# LinkedIn Voice Assistant 🎤

An intelligent voice-controlled assistant that automates LinkedIn outreach using OpenAGI and tracks all interactions in a spreadsheet.

## Features

- 🎤 **Voice Control**: Speak your commands naturally
- 🤖 **AI Automation**: Uses OpenAGI to automate LinkedIn interactions
- 📊 **Automatic Tracking**: Records all outreach in Google Sheets or CSV
- 💬 **Smart Messaging**: Sends personalized connection requests with notes
- ⚡ **Batch Processing**: Reach out to multiple people at once

## Installation

### 1. Prerequisites

- Python 3.8 or higher
- macOS with microphone access
- LinkedIn account (logged in on your default browser)
- OpenAGI API key

### 2. Install Dependencies

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Install PyAudio (required for voice recognition on macOS)
brew install portaudio
pip install pyaudio
```

### 3. Set Up OpenAGI API Key

```bash
export OAGI_API_KEY=your_api_key_here
```

Or add it to your `.env` file:
```
OAGI_API_KEY=your_api_key_here
```

### 4. (Optional) Google Sheets Setup

If you want to use Google Sheets instead of local CSV:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Sheets API and Google Drive API
4. Create service account credentials
5. Download the JSON credentials file
6. Save it as `credentials.json` in the project directory
7. Share your Google Sheet with the service account email

## Usage

### Basic Usage (Local CSV Tracking)

```bash
python voice_linkedin_assistant.py
```

### With Google Sheets

```bash
python voice_linkedin_assistant.py --google-sheets
```

### Voice Commands

Speak naturally! Examples:

- "Reach out to 10 people from Google regarding the Software Engineer position"
- "Contact 5 people at Microsoft about the Product Manager role"
- "Send connection requests to 15 people from Amazon for the Data Scientist position"

The assistant will:
1. Listen to your command
2. Parse the company, position, and number of people
3. Confirm with you before proceeding
4. Automate the LinkedIn outreach
5. Save all contacts to your spreadsheet

## Project Structure

```
HackNigh/
├── voice_linkedin_assistant.py   # Main application
├── voice_interface.py             # Voice recognition module
├── linkedin_automation.py         # LinkedIn automation with OpenAGI
├── spreadsheet_tracker.py         # Spreadsheet tracking (Google Sheets + CSV)
├── app.py                         # Original OpenAGI example
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## How It Works

### 1. Voice Input
The `VoiceInterface` class uses Google Speech Recognition to convert your voice to text:
- Listens through your microphone
- Converts speech to text
- Provides text-to-speech feedback

### 2. LinkedIn Automation
The `LinkedInAutomation` class uses OpenAGI's TaskerAgent:
- Searches for people at the specified company
- Clicks "Connect" or "More > Connect"
- Adds a personalized note to each request
- Handles LinkedIn's UI and connection limits

### 3. Spreadsheet Tracking
The tracking system records:
- Timestamp of outreach
- Company name
- Position applied for
- Contact name and title
- Connection status
- Message sent
- Response status
- Notes

## Modules

### voice_interface.py
Handles all voice interactions:
- `listen()`: Capture voice input
- `speak()`: Provide audio feedback
- `confirm()`: Yes/no questions

### linkedin_automation.py
Manages LinkedIn automation:
- `reach_out_to_connections()`: Structured outreach
- `reach_out_simple()`: Natural language processing

### spreadsheet_tracker.py
Tracks outreach data:
- `SpreadsheetTracker`: Google Sheets integration
- `LocalSpreadsheetTracker`: CSV file fallback

## Troubleshooting

### Microphone Issues
```bash
# Grant microphone permissions in System Preferences > Security & Privacy > Privacy > Microphone
```

### PyAudio Installation Issues
```bash
# Make sure you have portaudio installed
brew install portaudio
pip install --upgrade pyaudio
```

### LinkedIn Connection Limits
LinkedIn limits connection requests. The automation respects these limits and will note any warnings.

### Google Sheets Authentication
Make sure:
- Service account JSON file is named `credentials.json`
- It's in the project root directory
- Your spreadsheet is shared with the service account email

## Tips

1. **Start Small**: Test with 2-3 people before running larger batches
2. **Be Specific**: Clearly state the company name and position
3. **Check LinkedIn**: Monitor your LinkedIn account during automation
4. **Personalize Messages**: Edit the custom message template in `linkedin_automation.py`
5. **Respect Limits**: LinkedIn has weekly connection limits (~100-200)

## Customization

### Custom Connection Message
Edit the message template in `linkedin_automation.py`:

```python
custom_message = f"""Hi [Name],

Your custom message here mentioning {company_name} and {position_title}.

Best regards"""
```

### Change Voice Settings
Adjust in `voice_interface.py`:

```python
self.engine.setProperty('rate', 150)    # Speech speed
self.engine.setProperty('volume', 0.9)  # Volume
```

## Safety & Ethics

- Always comply with LinkedIn's Terms of Service
- Don't spam people with connection requests
- Use meaningful, personalized messages
- Respect daily/weekly connection limits
- Be genuine in your outreach

## Example Workflow

1. **Start the assistant**:
   ```bash
   python voice_linkedin_assistant.py
   ```

2. **Give a voice command**:
   > "Reach out to 10 people from Google about the Software Engineer position"

3. **Confirm**:
   > Assistant: "I will reach out to 10 people from Google regarding the Software Engineer position. Is this correct?"
   > You: "Yes"

4. **Wait for automation**:
   The assistant will automate the LinkedIn outreach

5. **Check results**:
   - View `linkedin_outreach.csv` or your Google Sheet
   - All contacts are tracked with timestamps

## Future Enhancements

- [ ] Add follow-up message automation
- [ ] Integrate with CRM systems
- [ ] Add response tracking
- [ ] Support for InMail messages
- [ ] Multi-language support
- [ ] Email notification on responses

## License

MIT License - Feel free to modify and use for your job search!

## Support

For issues or questions, please check:
- OpenAGI documentation: [OpenAGI Docs](https://openagi.com/docs)
- LinkedIn automation best practices
- Voice recognition troubleshooting guides

---

**Good luck with your job search! 🚀**
