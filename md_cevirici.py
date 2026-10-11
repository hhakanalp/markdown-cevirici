"""
Markdown Çevirici
PDF, Word, PowerPoint, Excel, HTML ve diğer belgeleri Markdown (.md) formatına çevirir.
Microsoft MarkItDown kütüphanesini kullanır.
"""

import os
import sys
import threading
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

DESTEKLENEN = {
    ".pdf", ".docx", ".pptx", ".xlsx", ".xls", ".html", ".htm",
    ".csv", ".json", ".xml", ".epub", ".txt", ".msg", ".zip",
}

_md = None


def markitdown_al():
    """MarkItDown nesnesini ilk kullanımda oluşturur (açılışı hızlandırır)."""
    global _md
    if _md is None:
        from markitdown import MarkItDown
        _md = MarkItDown()
    return _md


def cevir(dosya: Path, hedef_klasor: Path | None) -> Path:
    sonuc = markitdown_al().convert(str(dosya))
    klasor = hedef_klasor or dosya.parent
    cikti = klasor / (dosya.stem + ".md")
    cikti.write_text(sonuc.text_content, encoding="utf-8")
    return cikti


class Uygulama(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Markdown Çevirici")
        self.geometry("640x460")
        self.minsize(520, 380)

        self.dosyalar: list[Path] = []
        self.hedef_klasor: Path | None = None
        self.son_klasor: Path | None = None

        cerceve = ttk.Frame(self, padding=14)
        cerceve.pack(fill="both", expand=True)

        ttk.Label(
            cerceve,
            text="Belgelerinizi Markdown'a çevirin",
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="w")
        ttk.Label(
            cerceve,
            text="PDF, Word, PowerPoint, Excel, HTML, EPUB, CSV ...",
            foreground="#666",
        ).pack(anchor="w", pady=(0, 10))

        dugmeler = ttk.Frame(cerceve)
        dugmeler.pack(fill="x")
        ttk.Button(dugmeler, text="Dosya seç...", command=self.dosya_sec).pack(side="left")
        ttk.Button(dugmeler, text="Klasör seç...", command=self.klasor_sec).pack(side="left", padx=6)
        ttk.Button(dugmeler, text="Listeyi temizle", command=self.temizle).pack(side="left")

        self.liste = tk.Listbox(cerceve, height=8, activestyle="none")
        self.liste.pack(fill="both", expand=True, pady=8)

        hedef = ttk.Frame(cerceve)
        hedef.pack(fill="x")
        self.ayni_klasor = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            hedef,
            text="Kaynak dosyanın yanına kaydet",
            variable=self.ayni_klasor,
            command=self.hedef_degisti,
        ).pack(side="left")
        self.hedef_etiket = ttk.Label(hedef, text="", foreground="#666")
        self.hedef_etiket.pack(side="left", padx=8)

        alt = ttk.Frame(cerceve)
        alt.pack(fill="x", pady=(10, 0))
        self.cevir_dugme = ttk.Button(alt, text="Çevir", command=self.baslat)
        self.cevir_dugme.pack(side="left")
        self.ac_dugme = ttk.Button(alt, text="Klasörü aç", command=self.klasoru_ac, state="disabled")
        self.ac_dugme.pack(side="left", padx=6)
        self.ilerleme = ttk.Progressbar(alt, mode="determinate")
        self.ilerleme.pack(side="left", fill="x", expand=True, padx=(6, 0))

        self.durum = ttk.Label(cerceve, text="Hazır.", foreground="#444")
        self.durum.pack(anchor="w", pady=(8, 0))

        # Uygulama simgesinin üzerine bırakılan dosyalar (komut satırı argümanları)
        for arg in sys.argv[1:]:
            self.ekle(Path(arg))

    # --- dosya listesi ---
    def ekle(self, yol: Path):
        if yol.is_dir():
            for p in sorted(yol.iterdir()):
                if p.is_file() and p.suffix.lower() in DESTEKLENEN:
                    self.ekle(p)
            return
        if yol.is_file() and yol not in self.dosyalar:
            self.dosyalar.append(yol)
            self.liste.insert("end", str(yol))
        self.durum.config(text=f"{len(self.dosyalar)} dosya seçili.")

    def dosya_sec(self):
        yollar = filedialog.askopenfilenames(
            title="Çevrilecek dosyaları seçin",
            filetypes=[
                ("Desteklenen belgeler", " ".join("*" + u for u in sorted(DESTEKLENEN))),
                ("Tüm dosyalar", "*.*"),
            ],
        )
        for y in yollar:
            self.ekle(Path(y))

    def klasor_sec(self):
        y = filedialog.askdirectory(title="Belgelerin bulunduğu klasörü seçin")
        if y:
            self.ekle(Path(y))

    def temizle(self):
        self.dosyalar.clear()
        self.liste.delete(0, "end")
        self.ilerleme["value"] = 0
        self.durum.config(text="Hazır.")

    def hedef_degisti(self):
        if self.ayni_klasor.get():
            self.hedef_klasor = None
            self.hedef_etiket.config(text="")
        else:
            y = filedialog.askdirectory(title="Markdown dosyaları nereye kaydedilsin?")
            if y:
                self.hedef_klasor = Path(y)
                self.hedef_etiket.config(text=str(self.hedef_klasor))
            else:
                self.ayni_klasor.set(True)

    # --- çeviri ---
    def baslat(self):
        if not self.dosyalar:
            messagebox.showinfo("Markdown Çevirici", "Önce dosya veya klasör seçin.")
            return
        self.cevir_dugme.config(state="disabled")
        self.ilerleme.config(maximum=len(self.dosyalar), value=0)
        threading.Thread(target=self.calistir, daemon=True).start()

    def calistir(self):
        basarili, hatalar = 0, []
        for i, dosya in enumerate(list(self.dosyalar)):
            self.after(0, self.durum.config, {"text": f"Çevriliyor: {dosya.name}"})
            try:
                cikti = cevir(dosya, self.hedef_klasor)
                self.son_klasor = cikti.parent
                basarili += 1
                self.after(0, self.isaretle, i, "✓")
            except Exception as e:
                hatalar.append(f"{dosya.name}: {e}")
                self.after(0, self.isaretle, i, "✗")
            self.after(0, self.ilerleme.config, {"value": i + 1})
        self.after(0, self.bitti, basarili, hatalar)

    def isaretle(self, i, isaret):
        metin = str(self.dosyalar[i])
        self.liste.delete(i)
        self.liste.insert(i, f"{isaret}  {metin}")
        self.liste.itemconfig(i, foreground="#1a7f37" if isaret == "✓" else "#c62828")

    def bitti(self, basarili, hatalar):
        self.cevir_dugme.config(state="normal")
        if self.son_klasor:
            self.ac_dugme.config(state="normal")
        self.durum.config(text=f"Bitti: {basarili} dosya çevrildi, {len(hatalar)} hata.")
        if hatalar:
            messagebox.showwarning("Bazı dosyalar çevrilemedi", "\n".join(hatalar[:15]))

    def klasoru_ac(self):
        if not self.son_klasor:
            return
        if sys.platform.startswith("win"):
            os.startfile(self.son_klasor)
        elif sys.platform == "darwin":
            subprocess.run(["open", str(self.son_klasor)])
        else:
            subprocess.run(["xdg-open", str(self.son_klasor)])


if __name__ == "__main__":
    Uygulama().mainloop()
