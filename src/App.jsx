import React, { useState } from "react";
import "./index.css";

const App = () => {
  const [inputText, setInputText] = useState(""); // Store input text
  const [gifs, setGifs] = useState([]); // Store GIF URLs
  const [error, setError] = useState(""); // Store error messages

  // Handle change of input field
  const handleInputChange = (e) => {
    setInputText(e.target.value);
  };

  const handleTranslate = async () => {
    setError("");
    setGifs([]);
  
    try {
      // Use the full backend URL (ensure the backend is running at this address)
      const response = await fetch("http://127.0.0.1:5000/translate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: inputText }), // Send input text
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
      }
    } catch (err) {
      console.error("Error fetching GIFs:", err);
      setError("An error occurred while fetching GIFs. Please try again.");
    }
  };
  

  return (
    <>
    <div style={styles.container} className="everything">
      <div className="all">
      <h1>English to Sign Language <br /><span className="orange"> Translation </span>system</h1>
      <div style={styles.inputContainer}>
        <input
          type="text"
          value={inputText}
          onChange={handleInputChange}
          placeholder="Type text to translate..."
        />
        <br />
        <button onClick={handleTranslate} style={styles.button}>
          Translate
        </button>
      </div>
      

      {/* Display error message */}
      {error && <p style={styles.error}>{error}</p>}
      </div>
      </div>
      {/* Display GIFs */}
      <div id="displayer">
      <span className="cross">x</span>
        {gifs.map((gif, index) => (
          
          <img
            key={index}
            src={gif}
            alt={`Sign language GIF ${index + 1}`}
            style={styles.gif}
            className="finalgif"
          />
        ))}
      </div>
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
  input: {
    padding: "10px",
    fontSize: "16px",
    width: "300px",
    marginRight: "10px",
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
  gifContainer: {
    position: "absolute",
  },
  gif: {
    width: "500px",
    height: "300px",
    margin: "10px",
  },
  orange:{
    color:"rgb(249, 133, 1)",
  }


};

export default App;
