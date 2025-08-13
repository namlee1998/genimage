import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "./App.css";

function Result() {
  const location = useLocation();
  const navigate = useNavigate();
  const { imageUrl, fileName } = location.state || {};

  if (!imageUrl) {
    navigate("/");
    return null;
  }

  return (
    <div className="app">
      <h1 className="title">Your AI Image</h1>
      <img src={imageUrl} alt="Generated" className="generated-image" />
      <div className="button-group">
        <a href={imageUrl} download={fileName}>
          <button className="download-btn">Download</button>
        </a>
        <button className="back-btn" onClick={() => navigate("/")}>
          Generate Another
        </button>
      </div>
    </div>
  );
}

export default Result;
