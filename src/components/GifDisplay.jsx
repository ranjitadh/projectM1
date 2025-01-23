import React from "react";

const GifDisplay = ({ gifs }) => {
  return (
    <div>
      <h2>Translated Sign Language GIFs</h2>
      <div style={{ display: "flex", flexWrap: "wrap", gap: "10px" }}>
        {gifs.length > 0 ? (
          gifs.map((gif, index) => (
            <img 
              key={index} 
              src={`http://127.0.0.1:5000/static/${gif}`} 
              alt={`GIF for ${gif}`} 
              style={{ width: "200px", height: "200px", borderRadius: "10px" }} 
            />
          ))
        ) : (
          <p>No GIFs to display</p>
        )}
      </div>
    </div>
  );
};

export default GifDisplay;
