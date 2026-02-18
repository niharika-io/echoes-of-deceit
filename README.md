# Echoes of Deceit
**WIEgnite 3.0 Hackathon Project**

"Echoes of Deceit" is an immersive, voice-based interrogation simulator. Instead of relying on traditional text input, players act as detectives and use their real voice to question a virtual suspect. 
The system analyzes the player's vocal intensity (volume) and utilizes Natural Language Processing (Speech-to-Text) to detect specific case clues. If the detective shouts or catches the suspect in a lie using the right keywords, the suspect's psychological stress meter rises until they crack and confess.

# Core Features
Real-Time Vocal Analysis: Calculates the Root Mean Square (RMS) of the player's microphone input to measure intimidation and volume.
AI Keyword Detection: Uses Google's SpeechRecognition API to transcribe audio and hunt for case-specific clues (e.g., "bank", "money").
Dynamic Suspect Reactions: The virtual suspect's dialogue and visual stress levels change based on how loud the player speaks and what evidence is presented.
Custom UI: A sleek, dark-mode desktop interface built entirely in Python using Tkinter.

#Tech Stack
This project was built entirely in Python using the following libraries:
* Tkinter & Pillow (UI and Image Rendering)
* sounddevice & numpy (Microphone access and audio math processing)
* SpeechRecognition & scipy (Audio transcription and temporary file handling)
* pyaudio (Hardware audio interfacing)

# How to Run the Game
1. Clone this repository or download the ZIP file.
2. Open your terminal and navigate to the project folder.
3. Install the required dependencies by running:
   pip install -r requirements.txt
4. Run the main game file:
   python main.py
5. Put on your detective hat, click the "Interrogate" button, and start talking!

#System Calibration & Testing
To ensure the game functions perfectly in a loud hackathon environment, we conducted accuracy testing:
Background Noise: Recalibrated the RMS volume threshold to >60 to filter out ambient hall chatter.
Voice Variance:Tested across 3 different team members to ensure the NLP accurately picked up different accents and pitches (Achieved 90% accuracy).
Speech Speed Checks:Identified a drop to 60% accuracy during rapid speech, leading us to implement UI prompts guiding players to speak clearly.

