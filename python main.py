import tkinter as tk
from tkinter import ttk
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import os
from PIL import Image, ImageTk  

class InterrogationGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Echoes of Deceit - Interrogation Room")
        self.root.geometry("700x750") 
        self.root.configure(bg="#1e1e1e") 

        self.suspect_stress = 0
        self.keywords = ["bank", "money", "guard", "night", "camera", "stole","knife"]
        self.found_clues = []

        # --- UI ELEMENTS ---
        self.title_label = tk.Label(root, text="INTERROGATION ACTIVE", font=("Courier", 22, "bold"), fg="red", bg="#1e1e1e")
        self.title_label.pack(pady=10)

        # --- NEW: SUSPECT IMAGE ---
        try:
            # It tries to find 'suspect.png' in your folder
            img = Image.open("suspect.png")
            img = img.resize((180, 180), Image.Resampling.LANCZOS)
            self.suspect_img = ImageTk.PhotoImage(img)
            self.img_label = tk.Label(root, image=self.suspect_img, bg="#1e1e1e", bd=2, relief="solid")
        except FileNotFoundError:
            # If you haven't saved an image yet, it shows this cool placeholder box!
            self.img_label = tk.Label(root, text="[ MISSING FILE: suspect.png ]\nSave an image in this folder", 
                                      bg="#333333", fg="red", font=("Courier", 10, "bold"), width=30, height=10, bd=2, relief="solid")
        self.img_label.pack(pady=10)

        # Suspect Dialogue
        self.dialogue_label = tk.Label(root, text='"I want my lawyer."', font=("Arial", 16, "italic"), fg="white", bg="#1e1e1e")
        self.dialogue_label.pack(pady=10)

        # Stress Meter
        self.stress_label = tk.Label(root, text="Polygraph Stress Level:", font=("Arial", 10), fg="gray", bg="#1e1e1e")
        self.stress_label.pack()
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=5)

        # --- NEW: BIG VOLUME DISPLAY ---
        self.volume_display = tk.Label(root, text="VOCAL INTENSITY: 0", font=("Courier", 18, "bold"), fg="#aaaaaa", bg="#1e1e1e")
        self.volume_display.pack(pady=10)

        # Interaction Button
        self.interrogate_btn = tk.Button(root, text="🎤 INTERROGATE (5 Seconds)", font=("Arial", 14, "bold"), bg="darkred", fg="white", command=self.interrogate)
        self.interrogate_btn.pack(pady=15)

        self.status_label = tk.Label(root, text="Ready. Click button to speak.", fg="gray", font=("Arial", 12), bg="#1e1e1e")
        self.status_label.pack()

        # Transcript & Clues
        self.transcript_label = tk.Label(root, text='Transcript: [AI Audio Feed]', font=("Courier", 11), fg="yellow", bg="#1e1e1e")
        self.transcript_label.pack(pady=10)
        
        self.clues_label = tk.Label(root, text='Keywords Hit: None', font=("Courier", 12, "bold"), fg="#00ff00", bg="#1e1e1e")
        self.clues_label.pack()

    # --- AUDIO & GAME LOGIC ---
    def interrogate(self):
        self.status_label.config(text="🔴 RECORDING... SPEAK NOW!", fg="red", font=("Arial", 14, "bold"))
        self.root.update() 

        # --- CHANGED: Now listens for 5 seconds instead of 3 ---
        duration = 5 
        fs = 44100 
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64')
        sd.wait() 

        self.status_label.config(text="⚙️ Analyzing speech and voice stress...", fg="cyan", font=("Arial", 12))
        self.root.update()

        # Calculate the volume 
        volume = np.sqrt(np.mean(recording**2)) * 1000 
        
        # Speech to Text Conversion
        audio_int16 = np.int16(recording * 32767)
        wav.write("temp_mic.wav", fs, audio_int16)

        recognizer = sr.Recognizer()
        recognized_text = ""
        try:
            with sr.AudioFile("temp_mic.wav") as source:
                audio_data = recognizer.record(source)
                recognized_text = recognizer.recognize_google(audio_data).lower()
        except sr.UnknownValueError:
            recognized_text = "[Garbled audio - Speak clearer]"
        except sr.RequestError:
            recognized_text = "[Wi-Fi Error - Could not connect to Speech AI]"
            
        if os.path.exists("temp_mic.wav"):
            os.remove("temp_mic.wav")

        self.transcript_label.config(text=f'You said: "{recognized_text}"')
        self.evaluate_turn(volume, recognized_text)

    def evaluate_turn(self, volume, text):
        stress_gain = 0
        dialogue = ""

        # --- UPDATE BIG VOLUME UI ---
        # Change color based on how loud you were!
        if volume > 60:
            vol_color = "#ff4444" # Red
        elif volume > 15:
            vol_color = "#ffffaa" # Yellow
        else:
            vol_color = "#aaaaaa" # Gray
            
        self.volume_display.config(text=f"VOCAL INTENSITY: {int(volume)}", fg=vol_color)

        # Keyword Logic
        words_spoken = text.split()
        matched_words = [word for word in words_spoken if word in self.keywords]

        for word in matched_words:
            if word not in self.found_clues:
                self.found_clues.append(word)
                stress_gain += 15 

        if self.found_clues:
            self.clues_label.config(text="Keywords Hit: " + " | ".join(self.found_clues))

        # Volume & Response Logic
        if matched_words:
            dialogue = f'"Wait, who told you about the {matched_words[0]}?! You have no proof!"'
        elif volume > 60:  
            stress_gain += 10
            dialogue = '"Okay, okay! Just stop yelling! I was near the scene!"'
        elif volume > 15: 
            stress_gain += 2
            dialogue = '"You can\'t prove anything with that tone..."'
        else: 
            stress_gain -= 5 
            dialogue = '"Are you even trying, Detective? Speak up."'

        # Apply stress
        self.suspect_stress += stress_gain
        self.suspect_stress = max(0, min(100, self.suspect_stress))
        self.progress["value"] = self.suspect_stress
        self.dialogue_label.config(text=dialogue)

        # Win Condition
        if self.suspect_stress >= 100:
            self.dialogue_label.config(text='"I DID IT! I CONFESS! JUST LET ME GO!"', fg="#00ff00", font=("Arial", 18, "bold"))
            self.interrogate_btn.config(state="disabled") 
            self.status_label.config(text="🚨 CASE SOLVED. CONFESSION SECURED.", fg="#00ff00", font=("Arial", 14, "bold"))
        else:
            self.status_label.config(text="Awaiting next question...", fg="gray", font=("Arial", 12))

if __name__ == "__main__":
    root = tk.Tk()
    app = InterrogationGame(root)
    root.mainloop()