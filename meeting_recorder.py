import tkinter as tk
import speech_recognition as sr
import threading
from datetime import datetime
from googletrans import Translator

# Global flag to control listening
is_listening = True

def recognize_speech():
    """Continuously recognize speech, update the caption, and save it with translation."""
    global is_listening
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    translator = Translator()
    file_name = f"captions_{datetime.now().strftime('%Y-%m-%d')}.txt"

    # Open the file with UTF-8 encoding to support all characters, including Chinese
    with microphone as source, open(file_name, "a", encoding="utf-8") as file:
        recognizer.adjust_for_ambient_noise(source)
        while is_listening:
            try:
                print("Listening...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                text = recognizer.recognize_google(audio, language="en-US")
                
                # Translate text to Chinese
                translation = translator.translate(text, dest='zh-cn').text
                display_text = f"EN: {text}\nZH: {translation}"
                update_caption(display_text)

                # Save both English and Chinese captions to file in UTF-8
                file.write(f"EN: {text}\nZH: {translation}\n\n")
                file.flush()  # Ensure immediate write to file
            except sr.WaitTimeoutError:
                update_caption("[No speech detected]")
            except sr.UnknownValueError:
                update_caption("[Speech not clear]")
            except sr.RequestError as e:
                update_caption(f"[API Error: {e}]")

def update_caption(text):
    """Update the text label with new captions."""
    caption_label.config(text=text)

def start_recognition_thread():
    """Start the speech recognition in a separate thread."""
    global is_listening
    is_listening = True  # Reset flag to start listening
    recognition_thread = threading.Thread(target=recognize_speech)
    recognition_thread.daemon = True
    recognition_thread.start()

def stop_recognition():
    """Stop the speech recognition."""
    global is_listening
    is_listening = False  # Set flag to False to stop the loop
    update_caption("[Captioning stopped]")

# GUI setup
app = tk.Tk()
app.title("Real-Time Caption with Translation")
app.geometry("800x250")

# Caption Label
caption_label = tk.Label(app, text="Captions will appear here...", font=("Arial", 16), wraplength=750, justify="center")
caption_label.pack(expand=True, fill="both")

# Start Button
start_button = tk.Button(app, text="Start Captioning", font=("Arial", 14), command=start_recognition_thread)
start_button.pack()

# Stop Button
stop_button = tk.Button(app, text="Stop Captioning", font=("Arial", 14), command=stop_recognition)
stop_button.pack()

app.mainloop()
