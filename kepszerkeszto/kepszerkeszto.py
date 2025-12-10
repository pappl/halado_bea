import string
from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image, ImageTk, ImageFilter 
import requests
import torch
from transformers import pipeline
from io import BytesIO
import os
import tkinter as tk
from tkinter import filedialog, messagebox

try:
    from PIL.Image import Resampling
    LANCZOS = Resampling.LANCZOS
except ImportError:
    LANCZOS = Image.LANCZOS

class KepSzerkeszto:
    def __init__(self, master):
        self.master = master
        master.title("Képszerkesztő alkalmazás")

        master.attributes('-fullscreen', True)
        master.bind('<Escape>', self.kilepes_teljes_kepernyobol)

        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.eredeti_kep = None
        self.megjelenitett_kep = None
        self.tk_kep = None

        self.canvas = tk.Canvas(master, bg="lightgray")
        self.canvas.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        info_label = tk.Label(master, text="Nyomd meg az ESC billentyűt a kilépéshez!", fg="black")
        info_label.grid(row=0, column=0, sticky="ew", pady=(10, 5))

        self.gomb_frame = tk.Frame(master)
        self.gomb_frame.grid(row=2, column=0, pady=(5, 10))

        self.ai_frame = tk.Frame(master)
        self.ai_frame.grid(row=3, column=0, pady=(5, 10))

        self.ai_frame2 = tk.Frame(master)
        self.ai_frame2.grid(row=4, column=0, pady=(5, 10))

        #gombok
        self.betoltes_gomb = tk.Button(self.gomb_frame, text="Kép Betöltés", command=self.kep_betoltese)
        self.betoltes_gomb.pack(side=tk.LEFT, padx=10)

        self.mentes_gomb = tk.Button(self.gomb_frame, text="Mentés", command=self.kep_mentese, state=tk.DISABLED)
        self.mentes_gomb.pack(side=tk.LEFT, padx=10)

        self.forgatas_gomb = tk.Button(self.gomb_frame, text="Forgatás 90°", command=self.kep_forgatasa, state=tk.DISABLED)
        self.forgatas_gomb.pack(side=tk.LEFT, padx=10)

        self.ai_gomb = tk.Button(self.ai_frame, text="Átalakítás", command=self.ai_atalakitas, state=tk.DISABLED)
        self.ai_gomb.pack(side=tk.LEFT, padx=10)

        self.entry_prompt_var = tk.StringVar()
        self.neg_prompt_var = tk.StringVar()
        self.entry_valtozas_var = tk.StringVar()
        self.entry_erosseg_var = tk.StringVar()
        #input
        self.prompt_label = tk.Label(self.ai_frame, text="Add meg az átalakítás utasítását!", fg="black")
        self.prompt_label.pack(side=tk.LEFT, padx=10)
        self.prompt_entry= tk.Entry(self.ai_frame,textvariable = self.entry_prompt_var, width= 100)
        self.prompt_entry.pack(side=tk.LEFT, padx=10)
        #negativ prompt
        self.neg_prompt_label = tk.Label(self.ai_frame, text="Add meg mit hagyjon ki (opcionális)!", fg="black")
        self.neg_prompt_label.pack(side=tk.LEFT, padx=10)
        self.neg_prompt_entry= tk.Entry(self.ai_frame,textvariable = self.neg_prompt_var, width= 40)
        self.neg_prompt_entry.pack(side=tk.LEFT, padx=10)
        #valtozas
        self.valtozas_label = tk.Label(self.ai_frame2, text="Változás (0-100)", fg="black")
        self.valtozas_label.pack(side=tk.LEFT, padx=10)
        self.valtozas_entry= tk.Entry(self.ai_frame2,textvariable = self.entry_valtozas_var, width= 10)
        self.valtozas_entry.pack(side=tk.LEFT, padx=10)
        #erosseg
        self.erosseg_label = tk.Label(self.ai_frame2, text="Erősség (0-100)", fg="black")
        self.erosseg_label.pack(side=tk.LEFT, padx=10)
        self.erosseg_entry= tk.Entry(self.ai_frame2,textvariable = self.entry_erosseg_var, width= 10)
        self.erosseg_entry.pack(side=tk.LEFT, padx=10)

    def kilepes_teljes_kepernyobol(self, event):
        self.master.attributes('-fullscreen', False)
        self.master.destroy() 

    def kep_megjelenitese(self):
        if self.megjelenitett_kep:
            self.master.update_idletasks()
            
            kep_szelesseg, kep_magassag = self.megjelenitett_kep.size
            canvas_szelesseg = self.canvas.winfo_width()
            canvas_magassag = self.canvas.winfo_height()

            ratio_w = canvas_szelesseg / kep_szelesseg
            ratio_h = canvas_magassag / kep_magassag
            ratio = min(ratio_w, ratio_h)
            
            new_width = int(kep_szelesseg * ratio)
            new_height = int(kep_magassag * ratio)
            
            if ratio > 1:
                self.current_scale = 1.0
                new_width = kep_szelesseg
                new_height = kep_magassag
            else:
                self.current_scale = ratio

            self.megjelenitett_kep_resized = self.megjelenitett_kep.resize(
                (new_width, new_height), LANCZOS
            )

            self.tk_kep = ImageTk.PhotoImage(self.megjelenitett_kep_resized)
            
            self.canvas.delete("all")
            
            self.x_offset = (canvas_szelesseg - new_width) // 2
            self.y_offset = (canvas_magassag - new_height) // 2
            
            self.canvas.create_image(self.x_offset, self.y_offset, anchor=tk.NW, image=self.tk_kep)

    def kep_betoltese(self):
        fajl_utvonal = filedialog.askopenfilename(
            defaultextension=".jpg",
            filetypes=[("Képfájlok", "*.jpg;*.jpeg;*.png;*.bmp")]
        )
        if fajl_utvonal:
            try:
                self.eredeti_kep = Image.open(fajl_utvonal)
                self.megjelenitett_kep = self.eredeti_kep.copy()
                self.master.update_idletasks() 
                self.kep_megjelenitese()
                
                self.mentes_gomb.config(state=tk.NORMAL)
                self.ai_gomb.config(state=tk.NORMAL)
                self.forgatas_gomb.config(state=tk.NORMAL)
                
            except Exception as e:
                messagebox.showerror("Hiba", f"Hiba a kép betöltésekor: {e}")

    def kep_mentese(self):
        if self.megjelenitett_kep:
            fajl_utvonal = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG fájl", "*.png"), ("JPEG fájl", "*.jpg;*.jpeg"), ("Minden fájl", "*.*")]
            )
            if fajl_utvonal:
                try:
                    self.megjelenitett_kep.save(fajl_utvonal)
                except Exception as e:
                    messagebox.showerror("Hiba", f"Hiba a mentéskor: {e}")

    def forditas_angolra(self, felhasznalo_prompt):
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
    def ai_atalakitas(self):
        model_id_or_path = "runwayml/stable-diffusion-v1-5"
        device = "cuda" if torch.cuda.is_available() else "cpu"

        #image-to-image pipeline betöltése
        pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id_or_path, torch_dtype=torch.float16 if device == "cuda" else torch.float32)
        pipe = pipe.to(device)

        # prompt és paraméterek beállítása
        felhaszn_prompt=self.entry_prompt_var.get()
        prompt=self.forditas_angolra(felhaszn_prompt) if felhaszn_prompt!="" else ""
        felhaszn_prompt=self.neg_prompt_var.get()
        negative_prompt=self.forditas_angolra(felhaszn_prompt) if felhaszn_prompt!="" else ""
        valtozas= float(self.entry_valtozas_var.get())/100.0
        erosseg=float(self.entry_erosseg_var.get())/100.0
        self.megjelenitett_kep = pipe(prompt=prompt,
                               negative_prompt=negative_prompt, 
                               image=self.megjelenitett_kep, 
                               strength=valtozas, 
                               guidance_scale=erosseg).images[0]
        self.kep_megjelenitese()
        self.entry_prompt_var.set("")
        self.neg_prompt_var.set("")
        self.entry_valtozas_var.set("")
        self.entry_erosseg_var.set("")

    def kep_forgatasa(self):
        if self.megjelenitett_kep:
            self.megjelenitett_kep = self.megjelenitett_kep.rotate(-90, expand=True)
            
            jelenlegi_szelesseg = self.canvas.winfo_width()
            jelenlegi_magassag = self.canvas.winfo_height()
            
            self.canvas.config(width=jelenlegi_magassag, height=jelenlegi_szelesseg)
            self.kep_megjelenitese()

if __name__ == "__main__":
    root = tk.Tk()
    app = KepSzerkeszto(root)
    root.mainloop()