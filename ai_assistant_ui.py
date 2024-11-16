import tkinter as tk
import pyttsx3
import speech_recognition as sr
import subprocess
import webbrowser
from datetime import datetime
from transformers import pipeline
from googleapiclient.discovery import build

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize GPT-Neo text-generation pipeline
try:
    generator = pipeline('text-generation', model='EleutherAI/gpt-neo-1.3B')
    print("GPT model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")

# Google Custom Search setup
API_KEY = 'AIzaSyD-k3hXqGerL8bIG4G6_gw-LV3lh1Uxeg0'  # Replace with your API key
CX = 'a4212b80ccb9f4436'  # Replace with your CSE ID

# Function to get personalized greeting based on the time of day
def personalized_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning"
    elif hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"

# Function to greet the user when the application starts
def greet_user():
    greeting_message = personalized_greeting()
    engine.say(greeting_message)
    engine.runAndWait()
    response_label.config(text=greeting_message)  # Display the greeting on the UI

# Function to start listening to user's voice input
def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            user_input = recognizer.recognize_google(audio)
            print(f"You said: {user_input}")  # Debug print statement
            input_field.delete(0, tk.END)
            input_field.insert(0, user_input)
            process_input(user_input)
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            engine.say("Sorry, I did not understand that.")
            engine.runAndWait()
        except sr.RequestError:
            print("Could not request results.")
            engine.say("Could not request results.")
            engine.runAndWait()

# Function to generate a clean GPT response
def generate_gpt_response(user_input):
    try:
        # Use the user input directly and keep the response concise
        result = generator(user_input, max_length=50, num_return_sequences=1, truncation=True)
        response = result[0]['generated_text']
        
        # Remove any extra phrases from the response
        response = response.replace("Assistant, please respond to:", "").strip()
        return response.split('\n')[0]  # Return only the first line if needed
    except Exception as e:
        print(f"Error generating response: {e}")
        return "I'm sorry, I couldn't generate a response."


# Function to search Google using the Custom Search API
def search_google(query):
    try:
        service = build("customsearch", "v1", developerKey=API_KEY)
        res = service.cse().list(q=query, cx=CX).execute()
        if 'items' in res:
            return res['items'][0]['snippet']  # Return the first search result snippet
        else:
            return "I couldn't find any relevant information."
    except Exception as e:
        print(f"Error during Google search: {e}")
        return "Sorry, I couldn't perform the search."

# Function to process commands
def process_input(user_input):
    response_label.config(text=f"Processing: {user_input}")

    # If the user query contains "what is" or "who is", use Google search
     # If the user query contains common Google search phrases, use the API
    if any(keyword in user_input.lower() for keyword in ["what is", "who is", "who was", "when is", "when was"]):
        google_response = search_google(user_input)
        if len(google_response) > 300:  # Truncate long responses to fit UI
         google_response = google_response[:300] + "..."
        print(f"Google Response: {google_response}")
        engine.say(google_response)
        engine.runAndWait()
        response_label.config(text=google_response)  # Display truncated response

    elif "open notepad" in user_input.lower():
        subprocess.Popen("notepad.exe")
        engine.say("Opening Notepad.")
        engine.runAndWait()
        response_label.config(text="Opening Notepad")
    elif "open youtube" in user_input.lower():
        webbrowser.open("https://www.youtube.com")
        engine.say("Opening YouTube.")
        engine.runAndWait()
        response_label.config(text="Opening YouTube")
    elif "open google" in user_input.lower():
        webbrowser.open("https://www.google.com")
        engine.say("Opening Google.")
        engine.runAndWait()
        response_label.config(text="Opening Google")
    elif "open gmail" in user_input.lower():
        webbrowser.open("https://mail.google.com")
        engine.say("Opening Gmail.")
        engine.runAndWait()
        response_label.config(text="Opening Gmail")
    elif "open spotify" in user_input.lower():
        webbrowser.open("https://open.spotify.com")
        engine.say("Opening Spotify.")
        engine.runAndWait()
        response_label.config(text="Opening Spotify")
    elif "open facebook" in user_input.lower():
        webbrowser.open("https://www.facebook.com")
        engine.say("Opening Facebook.")
        engine.runAndWait()
        response_label.config(text="Opening Facebook")
    elif "open twitter" in user_input.lower():
        webbrowser.open("https://www.twitter.com")
        engine.say("Opening Twitter.")
        engine.runAndWait()
        response_label.config(text="Opening Twitter")
    elif "open instagram" in user_input.lower():
        webbrowser.open("https://www.instagram.com")
        engine.say("Opening Instagram.")
        engine.runAndWait()
        response_label.config(text="Opening Instagram")
    elif "open linkedin" in user_input.lower():
        webbrowser.open("https://www.linkedin.com")
        engine.say("Opening LinkedIn.")
        engine.runAndWait()
        response_label.config(text="Opening LinkedIn")
    elif "what time is it" in user_input.lower():
        current_time = datetime.now().strftime("%H:%M")
        engine.say(f"The current time is {current_time}.")
        engine.runAndWait()
        response_label.config(text=f"The current time is {current_time}")  
    elif "shut down the pc" in user_input.lower() or "shutdown" in user_input.lower():
        engine.say("Shutting down the PC.")
        engine.runAndWait()
        subprocess.call("shutdown /s /t 1", shell=True)
        response_label.config(text="Shutting down the PC")
      
    else:
        # Use GPT-Neo for other queries
        gpt_response = generate_gpt_response(user_input)
        print(f"GPT Response: {gpt_response}")
        engine.say(gpt_response)
        engine.runAndWait()
        response_label.config(text=gpt_response)  # Display GPT response on the UI

# Function to start the app with a greeting
def start_app():
    greeting = personalized_greeting()
    engine.say(f"{greeting}, how can I assist you today?")
    engine.runAndWait()

# Create the main window with a futuristic theme
root = tk.Tk()
root.title("N.O.V.A AI Assistant")
root.geometry("600x400")
root.configure(bg="#121212")

# Apply a glowing effect to the text labels
heading = tk.Label(root, text="N.O.V.A AI Assistant", font=("Orbitron", 28, "bold"), fg="#00ffcc", bg="#121212",wraplength=500, justify="left")
heading.pack(pady=20)

# Input field for typing or displaying commands
input_field = tk.Entry(root, font=("Orbitron", 16), width=35, bg="#1e1e1e", fg="#ffffff", borderwidth=2, relief="solid")
input_field.pack(pady=10)

# Glowing button with hover effect
def on_enter(e):
    listen_button.config(bg="#0099ff")

def on_leave(e):
    listen_button.config(bg="#1f8aff")

listen_button = tk.Button(root, text="Activate Voice Command", font=("Orbitron", 14), bg="#1f8aff", fg="white", width=20, height=2, command=listen_for_command)
listen_button.pack(pady=10)
listen_button.bind("<Enter>", on_enter)
listen_button.bind("<Leave>", on_leave)

# Response label to show AI assistant’s response
response_label = tk.Label(root, text="", font=("Orbitron", 16), fg="#00ff90", bg="#121212")
response_label.pack(pady=20)

# Start the app with a greeting
start_app()

# Run the main loop
root.mainloop()
