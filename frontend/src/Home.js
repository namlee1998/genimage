import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./App.css";

function Home() {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      alert("Please enter a prompt!");
      return;
    }

    try {
      setLoading(true);
      const res = await fetch("http://localhost:8080/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt }),
      });

      if (!res.ok) throw new Error("Failed to generate image");

      // Backend trả về { image_url: "...", file_name: "..." }
      const data = await res.json();

      navigate("/result", { state: { imageUrl: data.image_url, fileName: data.file_name } });
    } catch (err) {
      console.error(err);
      alert("Error generating image");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <img src="/images/aihead.JPEG" alt="AI Head" className="ai-image" />
      <h1 className="title">AI Image Generator</h1>
      <input
        type="text"
        className="prompt-input"
        placeholder="What’s going on in your mind now, my friend?"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
      <button
        className="download-btn"
        onClick={handleGenerate}
        disabled={loading}
      >
        {loading ? "Generating..." : "Generate"}
      </button>
    </div>
  );
}

export default Home;
