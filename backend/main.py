from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
from controlnet_aux import OpenposeDetector
from PIL import Image
import torch
import random
import os
import shutil
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # hoặc chỉ domain frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        num_inference_steps=70,
        generator=generator
    ).images[0]
    
    output_path = os.path.join("backend/static", "aiimg.png")
    image.save(output_path)
    return output_path

# ===== FastAPI app =====
app = FastAPI()
app.mount("/", StaticFiles(directory="backend/static", html=True), name="static")

@app.post("/generate")
def generate(data: dict):
    prompt = data.get("prompt")
    print(f"Generating image for: {prompt}")

    output_path = generate_image(prompt)
    file_name = os.path.basename(output_path)
    image_url = f"http://localhost:8000/{file_name}"

    return JSONResponse({"image_url": image_url, "file_name": file_name})
