from flask import Flask, request, jsonify, Response
from PIL import Image, ImageTk
from flask_cors import CORS
import string
from nltk.stem import PorterStemmer
from werkzeug.utils import secure_filename
import os
from flask import send_from_directory
import requests
import time


app = Flask(__name__)
CORS(app, support_credentials=True)

GIF_DIRECTORY = "ISL_Gifs"

isl_gif = ['birthday', 'goodmorning', 'happy', 'thank you', 'apple']
stemmer = PorterStemmer()

# @app.route('/translate', methods=['POST'])
# # def translate():
#     data = request.json
#     input_text = data.get("text", "").lower()
    
#     # Remove punctuation and apply stemming
#     input_text = input_text.translate(str.maketrans('', '', string.punctuation))
#     stemmed_input = " ".join([stemmer.stem(word) for word in input_text.split()])

#     print(stemmed_input)

#     gif_paths = []
#     words = stemmed_input.split()

#     for word in words:
#         if word in isl_gif:
#             gif_paths.append(f"/ISL_Gifs/{word}.gif")

#     file_path = "ISL_Gifs/birthday.gif"

#     with open(file_path, 'rb') as f:
#         files = {'image': f}

#     return Response(response=file_content, status=200, mimetype="image/gif")

# Example ISL GIF path mapping
isl_gif = {
    "birthday": "ISL_Gifs/birthday.gif",
    "happy": "ISL_Gifs/happy.gif"
    # Add more word-to-GIF mappings here
}

@app.route('/translate', methods=['POST'])
def process_input():
    # Ensure JSON data is provided
    if not request.is_json:
        return jsonify({"error": "Invalid input format. JSON required."}), 400

    data = request.get_json()

    # Retrieve the input text
    input_text = data.get("text", "").lower()

    # Remove punctuation and apply stemming
    input_text = input_text.translate(str.maketrans('', '', string.punctuation))
    stemmed_input = " ".join([stemmer.stem(word) for word in input_text.split()])

    # Generate list of GIF paths based on stemmed words
    gif_paths = []
    words = stemmed_input.split()
    for word in words:
        if word in isl_gif:
            gif_paths.append(word)

    for gif_name in gif_paths:
            file_path = os.path.join(GIF_DIRECTORY, gif_name)
            if os.path.exists(file_path):
                # Read the GIF file
                with open(file_path, "rb") as f:
                    gif_data = f.read()
                    # Yield as a part of the response
                    yield (b"--frame\r\n"
                           b"Content-Type: image/gif\r\n\r\n" +
                           gif_data + b"\r\n")
                # Add a delay between GIFs for streaming effect
                time.sleep(1)
            else:
                yield (b"--frame\r\n"
                       b"Content-Type: text/plain\r\n\r\n" +
                       f"GIF not found: {gif_name}\n".encode() +
                       b"\r\n")
    
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == '__main__':
    app.run(debug=True)





#     #from flask import Flask, request, jsonify, Response
# from flask_cors import CORS
# import string
# from nltk.stem import PorterStemmer
# import os
# import time

# app = Flask(__name__)
# CORS(app, support_credentials=True)

# UPLOAD_FOLDER = 'ISL_Gifs'  
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# isl_gif = {
#     "birthday": "birthday.gif",
#     "goodmorning": "goodmorning.gif",
#     "happy": "happy.gif",
#     "thankyou": "thankyou.gif",
#     "apple": "apple.gif"
# }
# stemmer = PorterStemmer()

# @app.route('/translate', methods=['POST'])
# def process_input():
#     # Ensure JSON data is provided
#     if not request.is_json:
#         return jsonify({"error": "Invalid input format. JSON required."}), 400

#     data = request.get_json()

#     # Retrieve the input text
#     input_text = data.get("text", "").lower()

#     # Remove punctuation and apply stemming
#     input_text = input_text.translate(str.maketrans('', '', string.punctuation))
#     stemmed_input = " ".join([stemmer.stem(word) for word in input_text.split()])

#     # Generate list of GIF paths based on stemmed words
#     gif_paths = []
#     words = stemmed_input.split()
#     for word in words:
#         if word in isl_gif:
#             gif_path = os.path.join(app.config['UPLOAD_FOLDER'], isl_gif[word])
#             if os.path.exists(gif_path):
#                 gif_paths.append(gif_path)

#     # Create a generator to stream GIFs
#     def generate():
#         for gif_path in gif_paths:
#             with open(gif_path, "rb") as f:
#                 gif_data = f.read()
#                 # Yield the GIF data as part of the response
#                 yield (b"--frame\r\n"
#                        b"Content-Type: image/gif\r\n\r\n" +
#                        gif_data + b"\r\n")
#             # Add a delay between GIFs for streaming effect
#             time.sleep(1)

#     # Return a streaming response with GIFs
#     return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


# if __name__ == '__main__':
#     app.run(debug=True)

    
