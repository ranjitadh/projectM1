import numpy as np
import matplotlib.pyplot as plt
import cv2
from easygui import *
import os
from PIL import Image, ImageTk
from itertools import count
import tkinter as tk
import string
from nltk.stem import PorterStemmer

def func(input_text=None):
    isl_gif = ['birthday', 'goodmorning', 'finish', 'goodevening', 'good afternoon', 'thank you', 'apple', 'bag', 'eat', 
               'happy', 'expire', 'find', 'great', 'man', 'move', 'mistake', 'night', 'open', 'over', 'once', 'only', 
               'other', 'please', 'pick', 'proper', 'quite', 'quit', 'run', 'rate', 'tough', 'tear', 'up', 'down', 
               'right', 'left', 'under', 'van', 'voice', 'text', 'sign', 'language', 'waste', 'sorry', 'what', 
               'wait', 'you', 'yes', 'no', 'year', 'zone','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
               'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    stemmer = PorterStemmer()

    while True:
        if not input_text:
            input_text = enterbox("Enter the text you want to convert to sign language:", "Text Input")
            if input_text is None:  # If user cancels
                return
        
        input_text = input_text.lower()
        print('You Entered: ' + input_text)

        # Remove punctuation
        for c in string.punctuation:
            input_text = input_text.replace(c, "")

        # Apply stemming to the input text
        stemmed_input = " ".join([stemmer.stem(word) for word in input_text.split()])

        if stemmed_input in ['goodbye', 'good bye', 'bye']:
            print("Oops! Time to say goodbye.")
            break

        elif stemmed_input in isl_gif:
            class ImageLabel(tk.Label):
                """A label that displays images and plays them if they are GIFs."""
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
                    except:
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

            root = tk.Tk()
            lbl = ImageLabel(root)
            lbl.pack()
            lbl.load(r'ISL_Gifs/{0}.gif'.format(input_text))
            root.mainloop()

        input_text = None  # Reset input for next iteration

    plt.close()

while True:
    image = "Homepage.png"
    msg = "HEARING IMPAIRMENT ASSISTANT"
    choices = ["Type Text", "All Done!"]
    reply = buttonbox(msg, image=image, choices=choices)

    if reply == choices[0]:
        func()  # Call the function to input text manually
    if reply == choices[1]:
        quit()
