from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image
import requests
import torch
from transformers import pipeline
from io import BytesIO
import os

def forditas_angolra(felhasznalo_prompt):
    classifier = pipeline(
        "zero-shot-classification", 
        model="facebook/bart-large-mnli",
        device="cuda" if torch.cuda.is_available() else "cpu"
    )
    nyelvek = ["Hungarian", "German", "French", "Spanish", "Italian"]

    result = classifier(
        felhasznalo_prompt, 
        nyelvek, 
        multi_label=False
    )
    felismert_nyelv = result['labels'][0]

    if felismert_nyelv == "Hungarian":
        model_nev = "Helsinki-NLP/opus-mt-hu-en"
    elif felismert_nyelv == "German":
        model_nev = "Helsinki-NLP/opus-mt-de-en"
    elif felismert_nyelv == "French":
        model_nev = "Helsinki-NLP/opus-mt-fr-en"
    elif felismert_nyelv == "Spanish":
        model_nev = "Helsinki-NLP/opus-mt-es-en"
    elif felismert_nyelv == "Italian":
        model_nev = "Helsinki-NLP/opus-mt-it-en"
    else:
        return felhasznalo_prompt

    fordito=pipeline("translation", model=model_nev)
    eredmeny= fordito(felhasznalo_prompt)
    angol_prompt=eredmeny[0]['translation_text']

    return angol_prompt
#modell betöltése
model_id_or_path = "runwayml/stable-diffusion-v1-5"
device = "cuda" if torch.cuda.is_available() else "cpu"

#image-to-image pipeline betöltése
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id_or_path, torch_dtype=torch.float16 if device == "cuda" else torch.float32)
pipe = pipe.to(device)

#bemeneti kép betöltése.
path=input("Adja meg a kép elérési útvonalát: ")
#C:\Users\Lili\Pictures\331e31d369af02328c60b02a4532b24e.png
init_image = Image.open(path).convert("RGB")
name=path.split('\\')[-1]
print(name)

#kép méretének csökkentése, ha túl nagy, hogy ne fogyasszon sok memóriát
#init_image = init_image.resize((768, 512))

# prompt és paraméterek beállítása
felhaszn_prompt=input("Kérlem írja le mit szeretne létrehozni: ")
prompt=forditas_angolra(felhaszn_prompt) if felhaszn_prompt!="" else ""
print(prompt)
felhaszn_prompt=input("Ha van valami amit el szeretne kerülni a képen, kérem adja meg: ")
negative_prompt=forditas_angolra(felhaszn_prompt) if felhaszn_prompt!="" else ""
valtozas= float(input("Kérem adja meg mennyire térjen el az eredeti képtől (0-50:kisebb változtatások;51-100: nagyobb eltérés az eredeti képtől): "))/100.0
erosseg=float(input("Kérem adja meg mennyire erősen kövesse az utasítást (0-100: magas értéken pontosabban követi az utasítást): "))/100.0
generated_image = pipe(prompt=prompt,
                       negative_prompt=negative_prompt, 
                       image=init_image, 
                       strength=valtozas, 
                       guidance_scale=erosseg).images[0]

generated_image.save(f"new_{name}")
print(f"A generált kép elmentve: new_{name}")
