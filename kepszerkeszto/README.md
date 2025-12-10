# Képszerkesztő alkalmazás

## Áttekintés

Ez egy Pythonban készült, grafikus felhasználói felülettel (Tkinter) rendelkező **képszerkesztő alkalmazás**, amely lehetővé teszi a felhasználók számára, hogy alapvető képszerkesztési műveleteket végezzenek. A program támogatja a klasszikus műveleteket (forgatás, vágás, átméretezés, színkorrekció), valamint AI-alapú átalakítást a Stable Diffusion Img2Img modell segítségével.

---

## Fő funkciók

### Kép betöltése és megjelenítése

* JPG, PNG, JPEG és BMP fájlok támogatása
* A kép automatikusan méreteződik a vászonhoz

### Visszavonás

* Legfeljebb **5 lépés** visszavonása
* Minden művelet automatikusan mentésre kerül az előzményhalmazba

### Kép forgatása

* A kép egyszerűen 90°-kal balra forgatható

### Kijelölés és vágás

* Egérrel húzható kijelölési téglalap
* A vágás a skálázás figyelembevételével pontosan történik

### Átméretezés

* Új szélesség és magasság megadása
* Opcionálisan az **arányok megtartása**

### Színkorrekció

* Fényerő, kontraszt és telítettség módosítása
* Élő előnézet külön ablakban

### AI-alapú átalakítás (Stable Diffusion Img2Img)

* A képen megadható átalakítási prompt
* Támogatott opcionális **negatív prompt**
* Két paraméter szabályozható:

  * **Változás mértéke (strength)**
  * **Útmutatás erőssége (guidance scale)**
* Automatikus nyelvfelismerés és angolra fordítás a promptokhoz

---

## Telepítés és futtatás

### 1. Könyvtárak telepítése

A projekt tartalmaz egy **requirements.txt** fájlt, amely felsorolja az összes szükséges csomagot.

```bash
pip install -r requirements.txt
```

### 2. Modell letöltése

A program automatikusan letölti a szükséges Stable Diffusion modellt (runwayml/stable-diffusion-v1-5). Ehhez internetkapcsolat kell.

### 3. Program futtatása

```bash
python kepszerkeszto.py
```

---

## Használati útmutató

1. Indítsd el az alkalmazást
2. Kattints a **Kép betöltése** gombra
3. Végezd el a szükséges szerkesztéseket:

   * forgatás
   * kijelölés + vágás
   * átméretezés
   * színkorrekció
4. AI-alapú átalakításhoz add meg a promptokat és a paramétereket
5. Kattints a **Mentés** gombra az eredmény elmentéséhez
6. A teljes képernyős módot ESC billentyűvel lehet elhagyni

---

## Fejlesztői információk

* Az alkalmazás figyelembe veszi a vászon méretét és automatikusan skálázza a képet
* A kijelölés és a vágás úgy lett implementálva, hogy a skálázott koordináták vissza legyenek számítva az eredeti kép koordinátáira
* Az AI átalakítás GPU-t használ, ha elérhető
