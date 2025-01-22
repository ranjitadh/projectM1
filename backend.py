from flask import Flask, request, jsonify
import string
from nltk.stem import PorterStemmer
from flask_cors import CORS
import os

app = Flask(__name__)

# Enable CORS for all origins
CORS(app)

# List of available GIFs
isl_gif = ['birthday', 'goodmorning', 'happy', 'thankyou', 'apple']

# Initialize Porter Stemmer for stemming
stemmer = PorterStemmer()

@app.route('/translate', methods=['POST'])
def translate():
    # Ensure JSON data is provided
    data = request.json
    if not data or "text" not in data:
        return jsonify({"error": "Invalid input"}), 400

    input_text = data.get("text", "").lower()
    
    # Remove punctuation and apply stemming
    input_text = input_text.translate(str.maketrans('', '', string.punctuation))
    stemmed_input = " ".join([stemmer.stem(word) for word in input_text.split()])

    gif_paths = []
    words = stemmed_input.split()

    # Match words with available GIFs
    for word in words:
        if word in isl_gif:
            gif_paths.append(f"/static/ISL_Gifs/{word}.gif")
    
    # Return the list of matching GIFs
    return jsonify({"gifs": gif_paths})

if __name__ == '__main__':
    app.run(debug=True)
