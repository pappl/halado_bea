from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image
import requests
import torch
from io import BytesIO
import os

#modell betöltése
model_id_or_path = "runwayml/stable-diffusion-v1-5"
device = "cuda" if torch.cuda.is_available() else "cpu"

#image-to-image pipeline betöltése
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id_or_path, torch_dtype=torch.float16 if device == "cuda" else torch.float32)
pipe = pipe.to(device)

#bemeneti kép betöltése.
path=r"C:\Users\Lili\Pictures\331e31d369af02328c60b02a4532b24e.png"
init_image = Image.open(path).convert("RGB")
name=path.split('\\')[-1]
print(name)

#kép méretének csökkentése, ha túl nagy, hogy ne fogyasszon sok memóriát
init_image = init_image.resize((768, 512))

# prompt és paraméterek beállítása
prompt = "Add a dinosaurus to the image"
negative_prompt="cat"
valtozas= 0.6
erosseg=0.6
generated_image = pipe(prompt=prompt,
                       negative_prompt=negative_prompt, 
                       image=init_image, 
                       strength=valtozas, 
                       guidance_scale=erosseg).images[0]

generated_image.save(f"new_{name}")
print(f"A generált kép elmentve: new_{name}")
