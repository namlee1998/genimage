import React, { useState } from "react";
import "./App.css";

function App() {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [audioUrl, setAudioUrl] = useState(null);

  const handleGenerate = async () => {
    setLoading(true);
    setAudioUrl(null);
    try {
      const response = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
      const data = await response.json();
      setAudioUrl(data.url);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <div className="container">
        <h1 className="title">AI Music Generator</h1>
        <textarea
          className="prompt-box"
          placeholder="Enter your prompt..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />
        <button className="generate-btn" onClick={handleGenerate} disabled={loading}>
          {loading ? "Generating..." : "Generate"}
        </button>
        {audioUrl && (
          <div className="player">
            <audio controls src={audioUrl}></audio>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
