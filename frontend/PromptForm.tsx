import { useState } from "react";

export default function PromptForm() {
  const [prompt, setPrompt] = useState("");
  const [status, setStatus] = useState("");
  const [ready, setReady] = useState(false);

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    setStatus("🧠 Đang sinh ảnh, xin chờ...");
    const formData = new FormData();
    formData.append("prompt", prompt);

    const res = await fetch("/generate", {
      method: "POST",
      body: formData
    });

    if (res.ok) {
      setStatus("✅ Hoàn tất!");
      setReady(true);
    } else {
      setStatus("❌ Lỗi xảy ra!");
    }
  };

return (
  <div className="flex flex-col items-center justify-center py-10 bg-gray-100 min-h-screen">
    {/* Hình ảnh trung tâm */}
    <div className="relative">
      <img
        src="./images/face-tech.jpg"
        alt="Futuristic face"
        className="w-full max-w-md rounded-xl shadow-lg object-cover"
      />
      {/* Tiêu đề trên ảnh, nếu cần overlay */}
      <div className="absolute top-4 left-4 text-white text-2xl font-bold drop-shadow-lg">
        AI Image Generator
      </div>
    </div>

    {/* Phần nhập prompt */}
    <div className="text-center p-8">
      <h1 className="text-xl font-semibold mb-4">
        What's going on in your mind now, my friend?
      </h1>
      <form onSubmit={handleSubmit} className="flex flex-col items-center gap-4">
        <input
          type="text"
          className="border border-gray-400 p-2 w-80 rounded"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          required
        />
        <button className="bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600">
          Generate
        </button>
        <p className="text-gray-600 italic">{status}</p>
        {ready && (
          <a
            href="/download"
            download
            className="bg-blue-600 text-white py-2 px-4 mt-4 rounded hover:bg-blue-700"
          >
            Download
          </a>
        )}
      </form>
    </div>
  </div>
);
}
