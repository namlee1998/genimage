import React from "react";
import { useLocation, useNavigate } from "react-router-dom";

function Result() {
  const location = useLocation();
  const navigate = useNavigate();
  const { imageUrl, fileName } = location.state || {};

  if (!imageUrl) {
    navigate("/");
    return null;
  }

  const handleDownload = () => {
    const a = document.createElement("a");
    a.href = imageUrl;
    a.download = fileName || "ai_image.png";
    a.click();
  };

  return (
    <div className="app">
      <h1>Your Generated Image</h1>
      <img src={imageUrl} alt="Generated" className="result-image" />
      <br />
      <button className="download-btn" onClick={handleDownload}>
        Download
      </button>
    </div>
  );
}

export default Result;
