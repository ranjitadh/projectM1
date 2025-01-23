from flask import Flask, request, jsonify, send_from_directory
from nltk.stem import PorterStemmer
from flask_cors import CORS
import os
import string

app = Flask(__name__)
CORS(app, origins=["http://localhost:5174"])
stemmer = PorterStemmer()

app.config['UPLOAD_FOLDER'] = 'ISL_Gifs'

# ISL words and phrases dataset
isl_gif = [
    'birthday','cry', 'good morning', 'finish', 'goodevening', 'good afternoon', 'thank you', 'goodnight', 'dad', 'dear',
    'happy', 'family', 'fine', 'great', 'man', 'move', 'mistake', 'night', 'open', 'over', 'once', 'only',
    'other', 'please', 'pick', 'proper', 'quite', 'quit', 'run', 'rate', 'tough', 'tear', 'up', 'down',
    'right', 'left', 'under', 'van', 'voice', 'where', 'sign', 'language', 'waste', 'sorry', 'what',
    'wait', 'you', 'yes', 'no', 'year', 'zone', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
    'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
]

# Dynamically generate a mapping of stemmed phrases and words to GIF filenames
stemmed_isl_gif = {stemmer.stem(word): f"{word.replace(' ', '_')}.gif" for word in isl_gif}

# Route to serve static GIF files
@app.route('/static/<filename>')
def serve_gif(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Main route for translation
@app.route('/translate', methods=['POST'])
def process_input():
    # Ensure JSON data is provided
    if not request.is_json:
        return jsonify({"error": "Invalid input format. JSON required."}), 400

    data = request.get_json()
    input_text = data.get("text", "").lower()

    # Remove punctuation from the input text
    input_text = input_text.translate(str.maketrans('', '', string.punctuation))

    # Log input text and processed words for debugging
    print(f"Processed input: {input_text}")

    # Check the whole stemmed input text against the dataset
    stemmed_input = stemmer.stem(input_text)
    gif_paths = []

    # Match stemmed input directly with phrases or split into words if no match is found
    if stemmed_input in stemmed_isl_gif:
        gif_paths.append(f"/static/{stemmed_isl_gif[stemmed_input]}")
    else:
        # Fall back to splitting the input and checking individual words
        for word in input_text.split():
            stemmed_word = stemmer.stem(word)
            if stemmed_word in stemmed_isl_gif:
                gif_paths.append(f"/static/{stemmed_isl_gif[stemmed_word]}")

    # If no GIFs are found for the given input text
    if not gif_paths:
        return jsonify({"error": "No GIFs found for the given text."}), 404

    # Return the paths of the GIFs
    return jsonify({"gifs": gif_paths})

if __name__ == '__main__':
    app.run(debug=True)
