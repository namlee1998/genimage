import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./App.css";

function Result() {
  const navigate = useNavigate();
  const [imageData, setImageData] = useState(null);

  useEffect(() => {
    const saved = localStorage.getItem("ai_image");
    if (saved) {
      setImageData(JSON.parse(saved));
    } else {
      navigate("/");
    }
  }, [navigate]);

  if (!imageData) return null;

  return (
    <div className="app">
      <h1 className="title">Your AI Image</h1>
      <img
        src={imageData.image_url}
        alt="Generated"
        className="generated-image"
      />
      <div className="button-group">
        <a href={imageData.image_url} download={imageData.file_name}>
          <button className="download-btn">Download</button>
        </a>
        <button
          className="back-btn"
          onClick={() => {
            localStorage.removeItem("ai_image");
            navigate("/");
          }}
        >
          Generate Another
        </button>
      </div>
    </div>
  );
}

export default Result;
