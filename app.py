from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS  # Import CORS for enabling cross-origin requests
import os
import string

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])  # Allow your React frontend to make requests

# Directory where GIF files are stored
app.config['UPLOAD_FOLDER'] = 'ISL_Gifs'  # Ensure your GIFs are placed inside the 'ISL_Gifs' folder

# Dictionary mapping words to corresponding GIF filenames
isl_gif = {
    "birthday": "birthday.gif",
    "goodmorning": "goodmorning.gif",
    "happy": "happy.gif",
    "thank you": "thankyou.gif",
    "apple": "apple.gif"
}

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

    # Generate a list of GIF paths based on the input words
    gif_paths = []
    for word in input_text.split():
        if word in isl_gif:
            # Log matched words for debugging
            print(f"Found match for word: {word}")
            gif_paths.append(f"/static/{isl_gif[word]}")  # Format the path to point to the /static/ directory

    # If no GIFs are found for the given input text
    if not gif_paths:
        return jsonify({"error": "No GIFs found for the given text."}), 404

    # Return the paths of the GIFs
    return jsonify({"gifs": gif_paths})

if __name__ == '__main__':
    app.run(debug=True)
