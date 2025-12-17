from flask import Flask, render_template, request, jsonify
import asyncio
import os
from datetime import datetime
import traceback
from io import BytesIO
from dotenv import load_dotenv

from oagi import AsyncScreenshotMaker
from oagi.agent.observer import AsyncAgentObserver
from oagi.agent.tasker import TaskerAgent
from oagi.handler import AsyncPyautoguiActionHandler

from spreadsheet_tracker import LocalSpreadsheetTracker
from elevenlabs.client import ElevenLabs

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize tracker
tracker = LocalSpreadsheetTracker("linkedin_outreach.csv")

# Initialize ElevenLabs client
elevenlabs_client = None
if os.getenv("ELEVENLABS_API_KEY"):
    elevenlabs_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    print("✅ ElevenLabs Speech-to-Text initialized")
else:
    print("⚠️  ELEVENLABS_API_KEY not found - speech-to-text will not work")


class LinkedInTasker:
    """LinkedIn automation using OpenAGI TaskerAgent"""
    
    def __init__(self):
        self.model = "lux-actor-1"
        self.max_steps = 30
        self.temperature = 0.0
        
    async def execute_linkedin_outreach(
        self, 
        company: str, 
        position: str, 
        num_people: int,
        command: str
    ):
        """
        Execute LinkedIn outreach automation
        
        Args:
            company: Company name to target
            position: Position title
            num_people: Number of people to reach out to
            command: Original voice command
            
        Returns:
            Dictionary with success status and results
        """
        try:
            # Setup observer for tracking
            observer = AsyncAgentObserver()
            image_provider = AsyncScreenshotMaker()
            action_handler = AsyncPyautoguiActionHandler()
            
            # Initialize TaskerAgent
            tasker = TaskerAgent(
                api_key=os.getenv("OAGI_API_KEY"),
                base_url=os.getenv("OAGI_BASE_URL", "https://api.agiopen.org"),
                model=self.model,
                max_steps=self.max_steps,
                temperature=self.temperature,
                step_observer=observer,
            )
            
            # Build instruction and todos
            instruction = (
                f"Go to LinkedIn and reach out to {num_people} people from {company} "
                f"regarding the {position} position. Send personalized connection requests with notes."
            )
            
            # Detailed todos for LinkedIn automation
            todos = [
                "Open LinkedIn in the browser (or switch to existing LinkedIn tab if already open)",
                f"Use the LinkedIn search bar to search for '{company}'",
                "Click on 'People' filter to show only people results from the company",
                "Scroll through the search results to view available profiles",
                f"IMPORTANT: You need to send EXACTLY {num_people} connection requests. Keep count as you go.",
                f"Initialize a counter starting at 0. Each time you successfully send a connection request, increment the counter by 1.",
                f"Repeat the following process ONLY until your counter reaches {num_people}, then STOP immediately:",
                "  - Look for the 'Connect' button on their profile card",
                "  - If 'Connect' is visible, click it directly",
                "  - If only 'More' (three dots) is visible, click it and select 'Connect' from dropdown",
                "  - When the connection dialog appears, look for 'Add a note' button",
                "  - Click 'Add a note' to open the message field",
                "  - Read their profile information: name, current role, company, and any visible experience or skills",
                f"  - Write a personalized message that is STRICTLY under 250 characters:",
                f"    * Use format: 'Hi [FirstName]! [Specific compliment about their work/role]. Exploring {position} at {company}. Would love to connect!'",
                f"    * Example: 'Hi Sarah! Your ML work at Meta is impressive. Exploring {position} roles at {company} and would love to connect. Open to a quick chat?'",
                f"    * Keep it under 200 characters to be safe - LinkedIn's limit is 300 but aim for 250 MAX",
                "  - CRITICAL: Check the character count shown at bottom of the note box",
                "  - If count shows over 250 characters, DELETE words until it's under 250",
                "  - Remove filler words: 'really', 'very', 'I think', 'I hope', etc.",
                "  - Only click 'Send' after confirming the message is under 250 characters",
                "  - Wait a moment for the request to be sent",
                "  - Increment your counter by 1 (you've now sent 1 more connection request)",
                f"  - Check if counter equals {num_people}. If yes, STOP IMMEDIATELY. If no, continue to next person.",
                f"After sending EXACTLY {num_people} connection requests, STOP the task completely. Do not send more.",
                "Handle any LinkedIn connection limit warnings by noting them",
                "If LinkedIn shows a warning about weekly invite limits, stop immediately and report the number completed"
            ]
            
            tasker.set_task(instruction, todos)
            
            print(f"🚀 Starting LinkedIn automation at {datetime.now()}")
            print(f"📋 Company: {company}")
            print(f"📋 Position: {position}")
            print(f"📋 Target: {num_people} people")
            print("=" * 60)
            
            # Execute the automation
            success = await tasker.execute(
                instruction="",
                action_handler=action_handler,
                image_provider=image_provider,
            )
            
            # Get execution summary
            memory = tasker.get_memory()
            status_summary = memory.get_todo_status_summary()
            completed = status_summary.get('completed', 0)
            
            print("\n" + "=" * 60)
            print("EXECUTION SUMMARY")
            print(f"Overall success: {success}")
            print(f"Completed todos: {completed}")
            print(memory.task_execution_summary)
            
            # Save execution history
            results_dir = "results/linkedin"
            os.makedirs(results_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(results_dir, f"linkedin_execution_{timestamp}.html")
            observer.export("html", output_file)
            print(f"📊 Exported execution history to {output_file}")
            
            # Add records to tracking spreadsheet
            records = []
            for i in range(num_people):
                records.append({
                    'company': company,
                    'position': position,
                    'name': f'Contact {i+1}',  # In production, extract from execution
                    'contact_title': 'Professional',
                    'status': 'Connection Sent',
                    'message_sent': 'Yes',
                    'response_status': 'Pending',
                    'notes': f'Voice command: {command}'
                })
            
            tracker.add_multiple_records(records)
            
            return {
                'success': success,
                'completed': completed,
                'total': num_people,
                'company': company,
                'position': position,
                'report_file': output_file
            }
            
        except Exception as e:
            print(f"❌ Error during LinkedIn automation: {e}")
            traceback.print_exc()
            return {
                'success': False,
                'error': str(e)
            }


@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template('index.html')


@app.route('/api/execute', methods=['POST'])
def execute():
    """
    API endpoint to execute LinkedIn automation
    
    Expected JSON body:
    {
        "command": "voice command text",
        "company": "company name",
        "position": "position title",
        "num_people": 10
    }
    """
    try:
        data = request.get_json()
        
        command = data.get('command', '')
        company = data.get('company', '')
        position = data.get('position', '')
        num_people = data.get('num_people', 10)
        
        if not company or not position:
            return jsonify({
                'success': False,
                'error': 'Company and position are required'
            }), 400
        
        # Validate num_people
        if not isinstance(num_people, int) or num_people < 1 or num_people > 50:
            return jsonify({
                'success': False,
                'error': 'Number of people must be between 1 and 50'
            }), 400
        
        # Execute automation in async context
        tasker = LinkedInTasker()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            tasker.execute_linkedin_outreach(company, position, num_people, command)
        )
        loop.close()
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': f"Successfully completed LinkedIn outreach to {company}",
                'data': result
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Unknown error occurred')
            }), 500
            
    except Exception as e:
        print(f"❌ API Error: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/transcribe', methods=['POST'])
def transcribe_audio():
    """
    API endpoint to convert audio to text using ElevenLabs
    
    Expected: multipart/form-data with 'audio' file
    """
    try:
        if not elevenlabs_client:
            return jsonify({
                'success': False,
                'error': 'ElevenLabs API key not configured'
            }), 500
        
        # Check if audio file is present
        if 'audio' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No audio file provided'
            }), 400
        
        audio_file = request.files['audio']
        
        if audio_file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Read audio data into BytesIO
        audio_data = BytesIO(audio_file.read())
        
        print(f"🎤 Transcribing audio file: {audio_file.filename}")
        
        # Convert speech to text using ElevenLabs
        transcription = elevenlabs_client.speech_to_text.convert(
            file=audio_data,
            model_id="scribe_v1",
            tag_audio_events=True,
            language_code="eng",
            diarize=False  # Set to True if multiple speakers
        )
        
        # Extract the text from the transcription
        transcript_text = transcription.text if hasattr(transcription, 'text') else str(transcription)
        
        print(f"✅ Transcription complete: {transcript_text[:100]}...")
        
        return jsonify({
            'success': True,
            'transcript': transcript_text,
            'full_response': {
                'text': transcript_text
            }
        })
        
    except Exception as e:
        print(f"❌ Transcription error: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/status')
def status():
    """Check API status"""
    api_key_set = bool(os.getenv("OAGI_API_KEY"))
    elevenlabs_key_set = bool(os.getenv("ELEVENLABS_API_KEY"))
    return jsonify({
        'status': 'online',
        'api_key_configured': api_key_set,
        'elevenlabs_configured': elevenlabs_key_set,
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    print("=" * 60)
    print("🎤 LinkedIn Voice Assistant Web Server")
    print("=" * 60)
    print("\nStarting Flask server...")
    print("Access the web interface at: http://localhost:5000")
    print("\nMake sure:")
    print("  ✓ OAGI_API_KEY is set in environment")
    print("  ✓ You're logged into LinkedIn in your browser")
    print("  ✓ Your browser window is visible")
    print("\n" + "=" * 60 + "\n")
    
    # Check API key
    if not os.getenv("OAGI_API_KEY"):
        print("⚠️  WARNING: OAGI_API_KEY not found in environment")
        print("Set it with: export OAGI_API_KEY=your_key_here\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
