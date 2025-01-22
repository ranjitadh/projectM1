import speech_recognition as sr
from easygui import *
import string
import os
from PIL import Image, ImageTk
from itertools import count
import tkinter as tk

# List of available sign language GIF words
def func(input_text=None):
    isl_gif = ['birthday', 'goodmorning', 'finish', 'goodevening', 'good afternoon', 'thank you', 'apple', 'bag', 'eat', 
               'happy', 'expire', 'find', 'great', 'man', 'move', 'mistake', 'night', 'open', 'over', 'once', 'only', 
               'other', 'please', 'pick', 'proper', 'quite', 'quit', 'run', 'rate', 'tough', 'tear', 'up', 'down', 
               'right', 'left', 'under', 'van', 'voice', 'text', 'sign', 'language', 'waste', 'sorry', 'what', 
               'wait', 'you', 'yes', 'no', 'year', 'zone','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
               'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# List of alphabet letters


def func_voice():
    """Function to handle live voice input"""
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        while True:
            print('Say something...')
            audio = r.listen(source)
            try:
                # Convert speech to text
                a = r.recognize_sphinx(audio).lower()
                print("You said: " + a)

                # Remove punctuation
                for c in string.punctuation:
                    a = a.replace(c, "")

                if a in ['goodbye', 'good bye', 'bye']:
                    print("Oops! Time to say goodbye.")
                    break

                process_input(a)

            except sr.UnknownValueError:
                print("Sorry, could not understand.")
            except sr.RequestError:
                print("Error connecting to speech recognition service.")
            except Exception as e:
                print(f"Error: {e}")

def func_text():
    """Function to handle live text input"""
    while True:
        text_input = enterbox("Enter text to convert to sign language:", "Live Text Input")
        if not text_input:
            break

        text_input = text_input.lower()

        # Remove punctuation
        for c in string.punctuation:
            text_input = text_input.replace(c, "")

        if text_input in ['goodbye', 'good bye', 'bye']:
            print("Oops! Time to say goodbye.")
            break

        process_input(text_input)

def process_input(input_text):
    """Process the given input text and play corresponding GIFs"""
    words = input_text.split()

    # Looping the sequence twice to repeat the GIFs
    for _ in range(2):  
        for word in words:
            if word in isl_gif:
                display_gif(f'ISL_Gifs/{word}.gif')
            else:
                for char in word:
                    if char in arr:
                        display_gif(f'letters/{char}.gif')

def display_gif(gif_path):
    """Function to display GIF animations"""
    class ImageLabel(tk.Label):
        """A label that displays and plays GIFs."""
        def load(self, im):
            if isinstance(im, str):
                im = Image.open(im)
            self.loc = 0
            self.frames = []

            try:
                for i in count(1):
                    self.frames.append(ImageTk.PhotoImage(im.copy()))
                    im.seek(i)
            except EOFError:
                pass

            try:
                self.delay = im.info['duration']
            except KeyError:
                self.delay = 100

            if len(self.frames) == 1:
                self.config(image=self.frames[0])
            else:
                self.next_frame()

        def unload(self):
            self.config(image=None)
            self.frames = None

        def next_frame(self):
            if self.frames:
                self.loc += 1
                self.loc %= len(self.frames)
                self.config(image=self.frames[self.loc])
                self.after(self.delay, self.next_frame)

    # Create Tkinter window to display the GIF
    root = tk.Tk()
    root.title("Sign Language Interpretation")
    lbl = ImageLabel(root)
    lbl.pack()
    lbl.load(gif_path)
    root.mainloop()

# Main program loop
while True:
    image = "Homepage.jpg"
    msg = "HEARING IMPAIRMENT ASSISTANT"
    choices = ["Live Voice", "Live Text", "All Done!"] 
    reply = buttonbox(msg, image=image, choices=choices)
    
    if reply == choices[0]:
        func_voice()
    elif reply == choices[1]:
        func_text()
    elif reply == choices[2]:
        quit()
