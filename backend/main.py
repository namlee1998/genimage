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

# =========================
# Thiết lập thiết bị
# =========================
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
TORCH_DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32

# =========================
# Load ảnh gốc
# =========================
IMAGE_PATH = os.getenv("IMAGE_PATH", "backend/trainimage.jpg")
input_image = Image.open(IMAGE_PATH).convert("RGB")

# =========================
# Tạo ảnh pose bằng OpenPose
# =========================
openpose = OpenposeDetector.from_pretrained("lllyasviel/ControlNet")
pose_image = openpose(input_image)

# =========================
# Load mô hình ControlNet + StableDiffusion
# =========================
controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/sd-controlnet-openpose",
    torch_dtype=TORCH_DTYPE
)

pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    controlnet=controlnet,
    torch_dtype=TORCH_DTYPE
).to(DEVICE)

# =========================
# Hàm sinh ảnh
# =========================
def generate_image(prompt: str, seed: int = None, negative_prompt: str = None) -> str:
    if seed is None:
        seed = random.randint(0, 100000)

    generator = torch.Generator(DEVICE).manual_seed(seed)

    # reset timesteps để kết quả ổn định
    pipe.scheduler.set_timesteps(50)

    image = pipe(
        prompt=prompt,
        image=pose_image,
        negative_prompt=negative_prompt or (
            "low quality, blurry, bad anatomy, missing facial features, "
            "ugly eyes, extra limbs, deformed hands"
        ),
        guidance_scale=8.5,
        num_inference_steps=50,
        generator=generator
    ).images[0]

    # Lưu ảnh ra thư mục backend/generated
    file_name = f"aiimg_{uuid.uuid4().hex}.png"
    output_dir = "backend/generated"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, file_name)
    image.save(output_path)

    return file_name

# =========================
# FastAPI App
# =========================
app = FastAPI()

# Middleware CORS (phòng trường hợp frontend/backend khác domain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static & generated
app.mount("/static", StaticFiles(directory="backend/static"), name="static")
app.mount("/generated", StaticFiles(directory="backend/generated"), name="generated")

# =========================
# API Endpoints
# =========================
@app.get("/api/status")
def status():
    return {"status": "ok"}

@app.post("/api/generate")
def generate(data: dict):
    prompt = data.get("prompt")
    if not prompt:
        return JSONResponse({"error": "Prompt is required"}, status_code=400)

    print(f"Generating image for: {prompt}")
    file_name = generate_image(prompt)
    image_url = f"/generated/{file_name}"

    return JSONResponse({"image_url": image_url, "file_name": file_name})

# =========================
# Serve React build
# =========================
frontend_dir = os.path.join(os.path.dirname(__file__), "build")
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
