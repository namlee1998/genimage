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
  <div className="flex flex-col items-center justify-center min-h-screen bg-yellow-200 p-6">
    {/* Ảnh AI */}
    <img
      src="/images/aihead.jpeg"
      alt="AI Head"
      className="w-60 h-60 mb-6 rounded-full shadow-lg object-cover"
    />

    {/* Tiêu đề */}
    <h1
      className="text-3xl font-bold mb-6"
      style={{
        textShadow: "2px 2px 4px #800080, -2px -2px 4px #ff0000",
      }}
    >
      AI Image Generator
    </h1>

    {/* Ô nhập prompt */}
    <input
      type="text"
      placeholder="What’s is going on in your mind now, my friend?"
      className="w-full max-w-md p-3 mb-10 border-2 border-gray-400 rounded-lg shadow-md text-center text-black focus:outline-none focus:border-purple-500"
    />

    {/* Nút Download */}
    <button className="px-6 py-2 bg-red-600 text-black font-bold rounded-full shadow-md hover:bg-red-700">
      Download
    </button>
  </div>
);

export default Home;
