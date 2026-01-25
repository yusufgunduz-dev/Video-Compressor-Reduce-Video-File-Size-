import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import threading
import asyncio
from app.core import video_processor
import sys

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class VideoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("GündüzAI Video Aracı")
        self.geometry("900x600")
        self.resizable(False, False)

        self.current_file = None
        self.info = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_area()

    def create_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="GündüzAI", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_select = ctk.CTkButton(self.sidebar_frame, text="Dosya Seç", command=self.select_file)
        self.btn_select.grid(row=1, column=0, padx=20, pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Tema:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 20))

    def create_main_area(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.info_frame = ctk.CTkFrame(self.main_frame)
        self.info_frame.pack(fill="x", pady=(0, 20))

        self.lbl_filename = ctk.CTkLabel(self.info_frame, text="Dosya seçilmedi", font=ctk.CTkFont(size=16))
        self.lbl_filename.pack(pady=10)
        
        self.lbl_details = ctk.CTkLabel(self.info_frame, text="")
        self.lbl_details.pack(pady=(0, 10))

        self.tabview = ctk.CTkTabview(self.main_frame)
        self.tabview.pack(fill="both", expand=True)

        self.tab_compress = self.tabview.add("Sıkıştır")
        self.tab_trim = self.tabview.add("Kes")

        self.create_compress_tab()
        self.create_trim_tab()

        self.progressbar = ctk.CTkProgressBar(self.main_frame)
        self.progressbar.pack(fill="x", pady=(20, 0))
        self.progressbar.set(0)

        self.lbl_status = ctk.CTkLabel(self.main_frame, text="Hazır")
        self.lbl_status.pack(pady=5)

    def create_compress_tab(self):
        frame = self.tab_compress
        
        ctk.CTkLabel(frame, text="Kalite (CRF): 18 (Yüksek) - 51 (Düşük)").pack(pady=(20, 5))
        
        self.slider_crf = ctk.CTkSlider(frame, from_=18, to=51, number_of_steps=34)
        self.slider_crf.pack(pady=5)
        self.slider_crf.set(36)
        
        self.lbl_crf_val = ctk.CTkLabel(frame, text="36")
        self.lbl_crf_val.pack(pady=0)
        
        self.slider_crf.configure(command=lambda v: self.lbl_crf_val.configure(text=f"{int(v)}"))

        ctk.CTkLabel(frame, text="Çözünürlük").pack(pady=(20, 5))
        self.option_res = ctk.CTkOptionMenu(frame, values=["Orijinal", "1920:-1", "1280:-1", "854:-1"])
        self.option_res.pack(pady=5)

        self.btn_compress = ctk.CTkButton(frame, text="Sıkıştır ve Kaydet", command=self.start_compress)
        self.btn_compress.pack(pady=30)

    def create_trim_tab(self):
        frame = self.tab_trim
        
        ctk.CTkLabel(frame, text="Başlangıç (sn)").pack(pady=(20, 5))
        self.entry_start = ctk.CTkEntry(frame)
        self.entry_start.pack(pady=5)
        self.entry_start.insert(0, "0")

        ctk.CTkLabel(frame, text="Bitiş (sn)").pack(pady=(20, 5))
        self.entry_end = ctk.CTkEntry(frame)
        self.entry_end.pack(pady=5)

        self.btn_trim = ctk.CTkButton(frame, text="Kes ve Kaydet", command=self.start_trim)
        self.btn_trim.pack(pady=30)

    def select_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Video", "*.mp4 *.mov *.avi *.mkv")])
        if filename:
            self.current_file = filename
            self.lbl_filename.configure(text=os.path.basename(filename))
            self.lbl_status.configure(text="Video analiz ediliyor...", text_color="yellow")
            threading.Thread(target=self.get_info_thread, daemon=True).start()

    def get_info_thread(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        info = loop.run_until_complete(video_processor.get_video_info(self.current_file))
        loop.close()
        
        self.after(0, self.update_info_ui, info)

    def update_info_ui(self, info):
        if "error" in info:
            self.lbl_details.configure(text="Hata: " + info["error"])
            self.lbl_status.configure(text="Hata", text_color="red")
        else:
            self.info = info
            size_mb = info['size'] / (1024 * 1024)
            details = f"{info['width']}x{info['height']} | {info['duration']:.1f} sn | {size_mb:.2f} MB"
            self.lbl_details.configure(text=details)
            self.entry_end.delete(0, "end")
            self.entry_end.insert(0, str(int(info['duration'])))
            self.lbl_status.configure(text="Hazır", text_color="white")

    def start_compress(self):
        if not self.current_file:
            return messagebox.showerror("Hata", "Lütfen önce bir dosya seçin.")
            
        default_name = f"{os.path.splitext(os.path.basename(self.current_file))[0]}_compressed.mp4"
        save_path = filedialog.asksaveasfilename(
            defaultextension=".mp4", 
            filetypes=[("MP4", "*.mp4")],
            title="Dosyayı Kaydet (Sıkıştırılmış)",
            initialfile=default_name
        )
        if not save_path:
            return

        crf = int(self.slider_crf.get())
        res_val = self.option_res.get()
        resolution = res_val if res_val != "Orijinal" else None

        self.lock_ui(True)
        self.progressbar.configure(mode="determinate")
        self.progressbar.set(0)
        self.lbl_status.configure(text="Sıkıştırılıyor... %0", text_color="blue")

        threading.Thread(target=self.compress_thread, args=(save_path, crf, resolution), daemon=True).start()

    def compress_thread(self, save_path, crf, resolution):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        def progress_callback(percentage):
             self.after(0, self.update_progress, percentage)

        result = loop.run_until_complete(video_processor.compress_video(self.current_file, save_path, crf, resolution, progress_callback))
        loop.close()
        self.after(0, self.finish_action, result)

    def update_progress(self, percentage):
        self.progressbar.set(percentage)
        self.lbl_status.configure(text=f"İşleniyor... %{int(percentage * 100)}")

    def start_trim(self):
        if not self.current_file:
            return messagebox.showerror("Hata", "Lütfen önce bir dosya seçin.")

        try:
            start = float(self.entry_start.get())
            end = float(self.entry_end.get())
        except ValueError:
            return messagebox.showerror("Hata", "Lütfen geçerli sayısal değerler girin.")

        default_name = f"{os.path.splitext(os.path.basename(self.current_file))[0]}_trimmed.mp4"
        save_path = filedialog.asksaveasfilename(
            defaultextension=".mp4", 
            filetypes=[("MP4", "*.mp4")],
            title="Dosyayı Kaydet (Kesilmiş)",
            initialfile=default_name
        )
        if not save_path:
            return

        self.lock_ui(True)
        self.progressbar.configure(mode="determinate") # İlerlemeli mod
        self.progressbar.set(0)
        self.lbl_status.configure(text="Kesiliyor... %0", text_color="blue")

        threading.Thread(target=self.trim_thread, args=(save_path, start, end), daemon=True).start()

    def trim_thread(self, save_path, start, end):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        def progress_callback(percentage):
             self.after(0, self.update_progress, percentage)

        result = loop.run_until_complete(video_processor.trim_video(self.current_file, save_path, start, end, progress_callback))
        loop.close()
        self.after(0, self.finish_action, result)

    def finish_action(self, result):
        self.progressbar.stop()
        self.progressbar.configure(mode="determinate")
        self.progressbar.set(1)
        self.lock_ui(False)

        if result.get("status") == "success":
            self.lbl_status.configure(text="İşlem Başarılı!", text_color="green")
            messagebox.showinfo("Başarılı", f"Dosya kaydedildi:\n{result['output_path']}")
        else:
            self.lbl_status.configure(text="Hata oluştu", text_color="red")
            messagebox.showerror("Hata", result.get("message"))

    def lock_ui(self, locked):
        state = "disabled" if locked else "normal"
        self.btn_select.configure(state=state)
        self.btn_compress.configure(state=state)
        self.btn_trim.configure(state=state)

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = VideoApp()
    app.mainloop()
