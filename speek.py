import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import edge_tts
import asyncio
import os
import threading
import pygame # Kita pakai pygame untuk preview suara di memori

# Inisialisasi mixer audio untuk preview
pygame.mixer.init()

class NunoVoicePro:
    def __init__(self, root):
        self.root = root
        self.root.title("NunoVoice Pro - Preview & Save")
        self.root.geometry("750x650")
        self.root.configure(bg="#0f172a")

        self.voice_map = {
            "Indonesia (Gadis - Soft)": "id-ID-GadisNeural",
            "Indonesia (Ardi - Bold)": "id-ID-ArdiNeural",
            "English (Guy - Reporter)": "en-US-GuyNeural",
            "English (Ava - Natural)": "en-US-AvaNeural",
            "Mandarin (Xiaoxiao)": "zh-CN-XiaoxiaoNeural",
            "Japanese (Nanami)": "ja-JP-NanamiNeural"
        }

        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self.root, bg="#1e293b")
        header.pack(fill="x")
        tk.Label(header, text="NUNOVOICE AI PREMIUM", font=("Segoe UI", 20, "bold"), fg="#38bdf8", bg="#1e293b").pack(pady=20)

        # Main Frame
        main_f = tk.Frame(self.root, bg="#0f172a")
        main_f.pack(fill="both", expand=True, padx=40, pady=20)

        tk.Label(main_f, text="Input Text:", fg="#94a3b8", bg="#0f172a").pack(anchor="w")
        self.txt_input = tk.Text(main_f, height=10, bg="#1e293b", fg="white", font=("Segoe UI", 11), insertbackground="white")
        self.txt_input.pack(fill="x", pady=5)

        tk.Label(main_f, text="Select Voice Character:", fg="#38bdf8", bg="#0f172a").pack(anchor="w", pady=(15,0))
        self.voice_select = ttk.Combobox(main_f, values=list(self.voice_map.keys()), state="readonly")
        self.voice_select.set("Indonesia (Gadis - Soft)")
        self.voice_select.pack(fill="x", pady=5)

        # Progress Bar
        self.progress = ttk.Progressbar(main_f, mode='indeterminate')
        self.progress.pack(fill="x", pady=20)

        # Tombol Aksi
        btn_f = tk.Frame(main_f, bg="#0f172a")
        btn_f.pack(pady=10)

        # Tombol Cek Suara (Preview)
        self.btn_preview = tk.Button(btn_f, text="▶ LISTEN PREVIEW", command=self.start_preview, 
                                     bg="#38bdf8", fg="#0f172a", font=("bold"), width=20, pady=10)
        self.btn_preview.pack(side="left", padx=10)

        # Tombol Generate (Save)
        self.btn_save = tk.Button(btn_f, text="💾 SAVE AS MP3", command=self.start_save, 
                                   bg="#059669", fg="white", font=("bold"), width=20, pady=10)
        self.btn_save.pack(side="left", padx=10)

    # --- LOGIKA PREVIEW ---
    def start_preview(self):
        teks = self.txt_input.get("1.0", tk.END).strip()
        if not teks: return
        self.progress.start()
        threading.Thread(target=lambda: asyncio.run(self.play_voice(teks)), daemon=True).start()

    async def play_voice(self, teks):
        try:
            voice = self.voice_map[self.voice_select.get()]
            temp_file = "preview_temp.mp3"
            communicate = edge_tts.Communicate(teks, voice)
            await communicate.save(temp_file)
            
            # Putar menggunakan pygame mixer
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy(): 
                continue # Tunggu sampai selesai putar
            pygame.mixer.music.unload()
            os.remove(temp_file) # Hapus file sampah
        finally:
            self.progress.stop()

    # --- LOGIKA SAVE ---
    def start_save(self):
        teks = self.txt_input.get("1.0", tk.END).strip()
        if not teks: return
        file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3", "*.mp3")])
        if file_path:
            self.progress.start()
            threading.Thread(target=lambda: asyncio.run(self.save_voice(teks, file_path)), daemon=True).start()

    async def save_voice(self, teks, path):
        try:
            voice = self.voice_map[self.voice_select.get()]
            communicate = edge_tts.Communicate(teks, voice)
            await communicate.save(path)
            messagebox.showinfo("Success", f"Audio saved successfully to:\n{path}")
        finally:
            self.progress.stop()

if __name__ == "__main__":
    root = tk.Tk()
    app = NunoVoicePro(root)
    root.mainloop()