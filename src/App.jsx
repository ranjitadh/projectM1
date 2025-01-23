import React, { useState } from "react";
import "./index.css";

const App = () => {
  const [inputText, setInputText] = useState(""); 
  const [gifs, setGifs] = useState([]); 
  const [error, setError] = useState(""); 
  const [currentGifIndex, setCurrentGifIndex] = useState(0); 
  const [isListening, setIsListening] = useState(false); 
  const [showModal, setShowModal] = useState(false); // Track modal visibility

  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();

  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.lang = "en-US";

  const handleInputChange = (e) => {
    setInputText(e.target.value);
  };

  const startListening = () => {
    setIsListening(true);
    setError(""); 
    recognition.start();

    recognition.onresult = (event) => {
      const spokenText = event.results[0][0].transcript;
      setInputText(spokenText); 
    };

    recognition.onerror = (event) => {
      console.error("Speech Recognition Error:", event.error);
      setError("Could not process speech. Try again.");
    };

    recognition.onend = () => {
      setIsListening(false);
    };
  };

  const handleTranslate = async () => {
    setError("");
    setGifs([]);
    setCurrentGifIndex(0);
    setShowModal(false); // Close modal before loading new translation

    try {
      const response = await fetch("http://127.0.0.1:5000/translate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: inputText }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      const gifUrls = result.gifs || [];
      const fullUrls = gifUrls.map((gif) => `http://127.0.0.1:5000${gif}`);

      if (fullUrls.length === 0) {
        setError("No GIFs found for the given text.");
      } else {
        setGifs(fullUrls);
        setShowModal(true); // Open modal
        sequentialGifPlayback(fullUrls); // Start GIF playback
      }
    } catch (err) {
      console.error("Error fetching GIFs:", err);
      setError("An error occurred while fetching GIFs. Please try again.");
    }
  };

  const sequentialGifPlayback = (gifUrls) => {
    const playGif = (index) => {
      if (index < gifUrls.length) {
        setCurrentGifIndex(index);
        setTimeout(() => {
          playGif(index + 1);
        }, 2000); // Delay between GIFs
      } else {
        setCurrentGifIndex(-1); // End GIF playback
      }
    };

    playGif(0);
  };

  return (
    <>
      <div style={styles.container} className="everything">
        <div className="all">
          <h1>
            English to Sign Language <br />
            <span className="orange">Translation</span> System
          </h1>
          <div style={styles.inputContainer}>
            <input
              type="text"
              value={inputText}
              onChange={handleInputChange}
              placeholder="Type text to translate..."
            />
            <button onClick={startListening} style={styles.micButton}>
              {isListening ? "Listening..." : "🎤"}
            </button>
            <br />
            <button onClick={handleTranslate} style={styles.button}>
              Translate
            </button>
          </div>

          {error && <p style={styles.error}>{error}</p>}
        </div>
      </div>

      {/* Modal for displaying GIFs */}
      {showModal && (
        <div style={styles.modalOverlay}>
          <div style={styles.modal}>
            <button
              style={styles.closeButton}
              onClick={() => setShowModal(false)} // Close the modal
            >
              &times;
            </button>
            {currentGifIndex !== -1 && gifs[currentGifIndex] && (
              <img
                src={gifs[currentGifIndex]}
                alt={`Sign language GIF ${currentGifIndex + 1}`}
                style={styles.gif}
                className="finalgif"
              />
            )}
          </div>
        </div>
      )}
    </>
  );
};

// Styles for the components
const styles = {
  container: {
    fontFamily: "Arial, sans-serif",
    textAlign: "center",
    padding: "20px",
  },
  inputContainer: {
    margin: "20px 0",
  },
  micButton: {
    padding: "10px",
    fontSize: "16px",
    cursor: "pointer",
    marginLeft: "10px",
  },
  button: {
    padding: "10px 20px",
    fontSize: "16px",
    cursor: "pointer",
  },
  error: {
    color: "red",
    marginTop: "10px",
  },
  gif: {
    width: "500px",
    height: "300px",
    margin: "10px",
  },
  orange: {
    color: "rgb(249, 133, 1)",
  },
  modalOverlay: {
    position: "fixed",
    top: 0,
    left: 0,
    width: "100%",
    height: "100%",
    backgroundColor: "rgba(0, 0, 0, 0.8)",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    zIndex: 1000,
  },
  modal: {
    backgroundColor: "white",
    padding: "20px",
    borderRadius: "8px",
    position: "relative",
    textAlign: "center",
  },
  closeButton: {
    position: "absolute",
    top: "10px",
    right: "10px",
    fontSize: "20px",
    cursor: "pointer",
    border: "none",
    background: "none",
  },
};

export default App;
