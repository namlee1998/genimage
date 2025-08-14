import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./App.css";

function Home() {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleGenerate = async () => {
    if (!prompt.trim()) return;
    setLoading(true);

    try {
      const res = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt })
      });

      const data = await res.json();
      // Lưu vào localStorage để reload không mất
      localStorage.setItem("ai_image", JSON.stringify(data));
      navigate("/result");
    } catch (err) {
      console.error(err);
      alert("Error generating image");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <h1 className="title">AI Image Generator</h1>
      <input
        type="text"
        placeholder="Enter your prompt..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        className="prompt-input"
      />
      <button onClick={handleGenerate} disabled={loading}>
        {loading ? "Generating..." : "Generate"}
      </button>
    </div>
  );
}

export default Home;
