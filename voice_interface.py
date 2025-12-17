import speech_recognition as sr
import pyttsx3
from typing import Optional


class VoiceInterface:
    """Voice interface for capturing user commands via speech recognition"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        
        # Configure text-to-speech
        self.engine.setProperty('rate', 150)  # Speed of speech
        self.engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        
    def speak(self, text: str):
        """Convert text to speech"""
        print(f"🔊 Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """
        Listen for voice input and convert to text
        
        Args:
            timeout: How long to wait for speech to start
            phrase_time_limit: Maximum time for a single phrase
            
        Returns:
            Transcribed text or None if no speech detected
        """
        with sr.Microphone() as source:
            print("🎤 Listening... (Speak now)")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            try:
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                
                print("🔄 Processing your speech...")
                text = self.recognizer.recognize_google(audio)
                print(f"📝 You said: {text}")
                return text
                
            except sr.WaitTimeoutError:
                print("⏱️ No speech detected within timeout period")
                return None
            except sr.UnknownValueError:
                print("❌ Could not understand audio")
                return None
            except sr.RequestError as e:
                print(f"❌ Speech recognition service error: {e}")
                return None
    
    def get_command(self, prompt: str = "What would you like me to do?") -> Optional[str]:
        """
        Get a voice command from the user
        
        Args:
            prompt: What to ask the user
            
        Returns:
            The user's command as text
        """
        self.speak(prompt)
        return self.listen()
    
    def confirm(self, question: str) -> bool:
        """
        Ask a yes/no question via voice
        
        Args:
            question: The question to ask
            
        Returns:
            True if user confirms, False otherwise
        """
        self.speak(question + " Say yes or no.")
        response = self.listen(timeout=5, phrase_time_limit=3)
        
        if response:
            response_lower = response.lower()
            return any(word in response_lower for word in ['yes', 'yeah', 'yep', 'sure', 'okay', 'ok'])
        
        return False


if __name__ == "__main__":
    # Test the voice interface
    voice = VoiceInterface()
    voice.speak("Voice interface initialized and ready!")
    
    command = voice.get_command("Please tell me what you'd like to do")
    if command:
        print(f"\nCaptured command: {command}")
        
        if voice.confirm("Did I understand you correctly?"):
            voice.speak("Great! Processing your command.")
        else:
            voice.speak("Let's try again.")
