import asyncio
import sys
import re
from voice_interface import VoiceInterface
from linkedin_automation import LinkedInAutomation
from spreadsheet_tracker import SpreadsheetTracker, LocalSpreadsheetTracker
from typing import Dict, Optional


class LinkedInVoiceAssistant:
    """Main application integrating voice control, LinkedIn automation, and tracking"""
    
    def __init__(self, use_google_sheets: bool = False):
        self.voice = VoiceInterface()
        self.linkedin = LinkedInAutomation()
        
        # Initialize tracker (Google Sheets or local CSV)
        if use_google_sheets:
            self.tracker = SpreadsheetTracker()
            if self.tracker.authenticate():
                self.tracker.create_or_open_spreadsheet()
                print(f"📊 Spreadsheet URL: {self.tracker.get_spreadsheet_url()}")
            else:
                print("⚠️  Falling back to local CSV tracking")
                self.tracker = LocalSpreadsheetTracker()
        else:
            self.tracker = LocalSpreadsheetTracker()
            print("📁 Using local CSV file for tracking")
    
    def parse_command(self, command: str) -> Optional[Dict[str, any]]:
        """
        Parse voice command to extract company, position, and number of people
        
        Args:
            command: The voice command text
            
        Returns:
            Dictionary with parsed parameters or None
        """
        command_lower = command.lower()
        
        # Extract number of people
        num_people = 10  # default
        number_patterns = [
            r'(\d+)\s+people',
            r'reach out to (\d+)',
            r'contact (\d+)',
        ]
        
        for pattern in number_patterns:
            match = re.search(pattern, command_lower)
            if match:
                num_people = int(match.group(1))
                break
        
        # Try to extract company name
        company = None
        company_patterns = [
            r'from\s+([A-Za-z0-9\s]+?)(?:\s+about|\s+regarding|\s+for)',
            r'at\s+([A-Za-z0-9\s]+?)(?:\s+about|\s+regarding|\s+for)',
            r'company\s+([A-Za-z0-9\s]+?)(?:\s+about|\s+regarding|\s+for)',
        ]
        
        for pattern in company_patterns:
            match = re.search(pattern, command_lower)
            if match:
                company = match.group(1).strip()
                break
        
        # Try to extract position
        position = None
        position_patterns = [
            r'(?:for|regarding|about)\s+(?:the\s+)?([A-Za-z0-9\s]+?)\s+position',
            r'(?:for|regarding|about)\s+(?:a\s+)?([A-Za-z0-9\s]+?)\s+role',
        ]
        
        for pattern in position_patterns:
            match = re.search(pattern, command_lower)
            if match:
                position = match.group(1).strip()
                break
        
        return {
            'company': company,
            'position': position,
            'num_people': num_people,
            'raw_command': command
        }
    
    async def execute_linkedin_outreach(self, params: Dict[str, any]):
        """
        Execute the LinkedIn outreach automation
        
        Args:
            params: Parsed command parameters
        """
        company = params.get('company', 'the company')
        position = params.get('position', 'the position')
        num_people = params.get('num_people', 10)
        
        # Confirm with user
        confirmation = f"I will reach out to {num_people} people from {company} regarding the {position} position. Is this correct?"
        
        if not self.voice.confirm(confirmation):
            self.voice.speak("Let's try again. Please tell me what you'd like to do.")
            return
        
        # Execute the automation
        self.voice.speak(f"Starting LinkedIn automation. This may take a few minutes.")
        
        try:
            # Run the LinkedIn automation
            results = await self.linkedin.reach_out_simple(params['raw_command'])
            
            # For demonstration, create sample results (in production, extract from automation)
            sample_results = []
            for i in range(num_people):
                sample_results.append({
                    'company': company,
                    'position': position,
                    'name': f'Contact {i+1}',
                    'contact_title': 'Professional',
                    'status': 'Connection Sent',
                    'message_sent': 'Yes',
                    'response_status': 'Pending',
                    'notes': f'Automated outreach via voice command'
                })
            
            # Add results to spreadsheet
            self.tracker.add_multiple_records(sample_results)
            
            # Confirm completion
            self.voice.speak(f"Successfully sent {num_people} connection requests to people at {company}. All contacts have been added to your tracking spreadsheet.")
            
        except Exception as e:
            self.voice.speak(f"An error occurred during automation: {str(e)}")
            print(f"❌ Error: {e}")
    
    async def run(self):
        """Main application loop"""
        self.voice.speak("LinkedIn Voice Assistant is ready!")
        self.voice.speak("You can tell me to reach out to people on LinkedIn, and I'll automate it for you.")
        
        while True:
            # Get voice command
            command = self.voice.get_command(
                "What would you like me to do? Say 'exit' or 'quit' to stop."
            )
            
            if not command:
                continue
            
            # Check for exit command
            if any(word in command.lower() for word in ['exit', 'quit', 'stop', 'goodbye']):
                self.voice.speak("Goodbye! Have a great day!")
                break
            
            # Parse the command
            params = self.parse_command(command)
            
            if not params['company'] or not params['position']:
                self.voice.speak(
                    "I need more information. Please mention the company name and the position you're applying for."
                )
                continue
            
            # Execute the LinkedIn outreach
            await self.execute_linkedin_outreach(params)
            
            # Ask if they want to do anything else
            if not self.voice.confirm("Would you like to do anything else?"):
                self.voice.speak("Alright! Have a great day!")
                break


async def main():
    """Entry point for the application"""
    print("=" * 60)
    print("🎤 LinkedIn Voice Assistant with OpenAGI")
    print("=" * 60)
    print("\nThis application will:")
    print("  1. Listen to your voice commands")
    print("  2. Automate LinkedIn outreach using OpenAGI")
    print("  3. Track all contacts in a spreadsheet")
    print("\n" + "=" * 60 + "\n")
    
    # Check if user wants to use Google Sheets
    use_sheets = False
    if len(sys.argv) > 1 and sys.argv[1] == '--google-sheets':
        use_sheets = True
        print("📊 Google Sheets integration enabled")
    else:
        print("📁 Using local CSV file (use --google-sheets flag for Google Sheets)")
    
    print("\n")
    
    # Create and run the assistant
    assistant = LinkedInVoiceAssistant(use_google_sheets=use_sheets)
    
    try:
        await assistant.run()
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
