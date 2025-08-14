from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
from controlnet_aux import OpenposeDetector
from PIL import Image
import torch
import random
import os
import uuid
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# ===== Thiết lập thiết bị =====
device = "cuda" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if device == "cuda" else torch.float32

# ===== Load ảnh gốc =====
IMAGE_PATH = os.getenv("IMAGE_PATH", "backend/trainimage.jpg")
input_image = Image.open(IMAGE_PATH).convert("RGB")

# ===== Tạo ảnh pose =====
openpose = OpenposeDetector.from_pretrained("lllyasviel/ControlNet")
pose_image = openpose(input_image)

# ===== Load mô hình ControlNet =====
controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/sd-controlnet-openpose",
    torch_dtype=torch_dtype
)
pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    controlnet=controlnet,
    torch_dtype=torch_dtype
).to(device)

# ===== Hàm sinh ảnh =====
def generate_image(prompt: str, seed=None, negative_prompt=None) -> str:
    if seed is None:
        seed = random.randint(0, 100000)
    generator = torch.Generator(device).manual_seed(seed)

    image = pipe(
        prompt=prompt,
        image=pose_image,
        negative_prompt=negative_prompt or "low quality, blurry, bad anatomy, missing facial features, ugly eyes, extra limbs, deformed hands",
        guidance_scale=8.5,
        num_inference_steps=50,
        generator=generator
    ).images[0]
    
    # Lưu file với UUID
    file_name = f"aiimg_{uuid.uuid4().hex}.png"
    output_path = os.path.join("backend/generated", file_name)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image.save(output_path)
    return file_name

# ===== FastAPI app =====
app = FastAPI()

# Middleware CORS (phòng trường hợp backend tách domain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/generate")
def generate(data: dict):
    prompt = data.get("prompt")
    print(f"Generating image for: {prompt}")

    file_name = generate_image(prompt)
    image_url = f"/generated/{file_name}"  # ảnh sẽ nằm trong /generated

    return JSONResponse({"image_url": image_url, "file_name": file_name})

# Serve ảnh sinh ra
app.mount("/generated", StaticFiles(directory="backend/generated"), name="generated")

# Serve frontend build
app.mount("/", StaticFiles(directory="backend/static", html=True), name="frontend")
