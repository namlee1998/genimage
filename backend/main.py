from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
from controlnet_aux import OpenposeDetector
from PIL import Image
import torch
import random
import os
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, JSONResponse
from genai import generate_image

device = "cuda" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if device == "cuda" else torch.float32

# ===== 📥 Load ảnh gốc nội bộ =====
IMAGE_PATH = os.getenv("IMAGE_PATH", "./trainimage.jpg") 
input_image = Image.open(os.path.join(image_folder, file)).convert("RGB")

# ===== 🧬 Tạo ảnh pose =====
openpose = OpenposeDetector.from_pretrained("lllyasviel/ControlNet")
pose_image = openpose(input_image)

# ===== 📦 Load mô hình ControlNet =====
controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/sd-controlnet-openpose",
    torch_dtype=torch_dtype
)

pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    controlnet=controlnet,
    torch_dtype=torch_dtype
).to(device)

# 🚀 Hàm sinh ảnh
def generate_image(prompt: str) -> str:
    if seed is None:
        seed = random.randint(0, 100000)
    generator = torch.Generator("cuda").manual_seed(seed)

    image = pipe(
        prompt=prompt,
        image=pose_image,
        negative_prompt=negative_prompt or "low quality, blurry, bad anatomy, missing facial features, ugly eyes, extra limbs, deformed hands",
        guidance_scale=8.5,
        num_inference_steps=70,
        generator=generator
    ).images[0]
    
    output_path = "output.png"
    image.save(output_path)

    return output_path

app = FastAPI()

app.mount("/", StaticFiles(directory="backend/static", html=True), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://cra-frontend-622933104662.asia-southeast1.run.app", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/generate")
def create_image(prompt: str = Form(...)):
    output_path = generate_image(prompt)
    return JSONResponse({"status": "success", "file": output_path})

@app.get("/download")
def download_image():
    return FileResponse("output.png", media_type="image/png", filename="result_image.png")