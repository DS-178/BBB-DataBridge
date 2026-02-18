import os
import sys
import subprocess
import platform
import json
import datetime
import threading
import time
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

from config import AppConfig
from logic import DataConverter

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(AppConfig.APP_NAME)
        self.geometry("750x550")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Cross-Platform Icon Loading (Safe Mode)
        if os.path.exists("logo.ico"):
            try:
                icon_img = Image.open("logo.ico")

                #WICHTIG: Auf eine sichere Größe verkleinern (z.B. 64x64)
                # Das verhindert den "BadLength"-Fehler unter Linux
                icon_img = icon_img.resize((64, 64), Image.Resampling.LANCZOS)

                self.wm_iconphoto(True, ImageTk.PhotoImage(icon_img))
            except Exception as e:
                print(f"Warnung: Icon konnte nicht geladen werden: {e}")

        self.input_filepath = None
        self.final_output_path = None
        self.log_visible = False
        self.is_processing = False

        self.settings = self.load_settings()
        self.converter = DataConverter(log_callback=self.log_message)

        self._init_ui()

    def load_settings(self):
        try:
            with open("settings.json", "r") as f: return json.load(f)
        except: return {"output_folder": os.path.expanduser("~\\Documents")}

    def save_settings(self):
        with open("settings.json", "w") as f: json.dump(self.settings, f)

    def _init_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(8, weight=1)

        f_head = ctk.CTkFrame(self, fg_color="transparent")
        f_head.grid(row=0, column=0, padx=30, pady=(25, 10), sticky="ew")
        ctk.CTkLabel(f_head, text="Export Tool", font=("Segoe UI", 28, "bold")).pack(anchor="w")
        ctk.CTkLabel(f_head, text="Pretix ➔ Datacool", font=("Segoe UI", 14), text_color="gray").pack(anchor="w")

        self.card_in = ctk.CTkFrame(self, fg_color=("gray90", "gray13"))
        self.card_in.grid(row=1, column=0, padx=30, pady=5, sticky="ew")

        self.entry_in = ctk.CTkEntry(self.card_in, placeholder_text="Quelldatei wählen...", height=40, border_width=0, fg_color="transparent")
        self.entry_in.pack(side="left", fill="x", expand=True, padx=15, pady=5)
        self.entry_in.configure(state="disabled")
        ctk.CTkButton(self.card_in, text="Datei auswählen", width=120, fg_color=("gray80", "gray20"), text_color=("black", "white"), hover_color=("gray70", "gray30"), command=self.select_input).pack(side="right", padx=10, pady=5)

        self.card_out = ctk.CTkFrame(self, fg_color=("gray90", "gray13"))
        self.card_out.grid(row=2, column=0, padx=30, pady=5, sticky="ew")

        self.entry_out = ctk.CTkEntry(self.card_out, placeholder_text="Zielordner...", height=40, border_width=0, fg_color="transparent")
        self.entry_out.pack(side="left", fill="x", expand=True, padx=15, pady=5)
        self.entry_out.insert(0, self.settings["output_folder"])
        self.entry_out.configure(state="disabled")
        ctk.CTkButton(self.card_out, text="Ziel ändern", width=100, fg_color=("gray80", "gray20"), text_color=("black", "white"), hover_color=("gray70", "gray30"), command=self.select_output_folder).pack(side="right", padx=10, pady=5)

        self.card_opt = ctk.CTkFrame(self, fg_color="transparent")
        self.card_opt.grid(row=3, column=0, padx=30, pady=(15, 5), sticky="ew")

        ctk.CTkLabel(self.card_opt, text="Filter:", font=("Segoe UI", 12, "bold"), text_color="gray").pack(side="left", padx=(0,10))

        self.seg_filter = ctk.CTkSegmentedButton(self.card_opt, values=["Alle", "Nur Bezahlt", "Nur Offen"])
        self.seg_filter.set("Alle")
        self.seg_filter.pack(side="left")

        ctk.CTkLabel(self.card_opt, text="(Stornierte werden immer entfernt)", font=("Segoe UI", 11), text_color="gray").pack(side="right")

        self.btn_start = ctk.CTkButton(self, text="Export Starten", font=("Segoe UI", 16, "bold"), height=50, corner_radius=10, command=self.start_process, state="disabled", fg_color="gray")
        self.btn_start.grid(row=4, column=0, padx=30, pady=15, sticky="ew")

        self.progress = ctk.CTkProgressBar(self, height=6, progress_color="#107C41")
        self.progress.grid(row=5, column=0, padx=30, pady=(0, 10), sticky="ew")
        self.progress.set(0)
        self.progress.grid_remove()

        self.f_success = ctk.CTkFrame(self, fg_color="transparent", height=0)
        self.f_success.grid(row=6, column=0, padx=30, pady=5, sticky="ew")
        self.f_success.grid_remove()
        self.btn_open = ctk.CTkButton(self.f_success, text="Excel Öffnen ↗", command=self.open_excel, fg_color="#107C41", hover_color="#0c5e31", height=45, corner_radius=22, font=("Segoe UI", 14, "bold"))

        self.f_footer = ctk.CTkFrame(self, fg_color="transparent")
        self.f_footer.grid(row=7, column=0, padx=30, pady=5, sticky="ew")
        self.lbl_status = ctk.CTkLabel(self.f_footer, text="Bereit.", text_color="gray")
        self.lbl_status.pack(side="left")
        self.btn_toggle_log = ctk.CTkButton(self.f_footer, text="Details anzeigen 🔽", fg_color="transparent", text_color=("gray50", "gray70"), hover=False, command=self.toggle_log, width=100)
        self.btn_toggle_log.pack(side="right")

        self.log_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.log_box = ctk.CTkTextbox(self.log_frame, font=("Consolas", 11), height=150, corner_radius=10)
        self.log_box.pack(fill="both", expand=True)
        self.log_box.configure(state="disabled")

    def toggle_log(self):
        if self.log_visible:
            self.log_frame.grid_forget()
            self.btn_toggle_log.configure(text="Details anzeigen 🔽")
            h = 630 if self.f_success.winfo_ismapped() else 550
            self.geometry(f"750x{h}")
            self.log_visible = False
        else:
            self.geometry("750x700")
            self.after(100, lambda: self.log_frame.grid(row=8, column=0, padx=30, pady=(0, 20), sticky="nsew"))
            self.btn_toggle_log.configure(text="Details verbergen 🔼")
            self.log_visible = True

    def smooth_progress_loop(self):
        if not self.is_processing: return
        current_val = self.progress.get()
        new_val = current_val + 0.015
        if new_val > 1: new_val = 0
        self.progress.set(new_val)
        self.after(20, self.smooth_progress_loop)

    def log_message(self, message):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[{ts}] {message}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")
        self.lbl_status.configure(text=message)

    def select_input(self):
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if path:
            self.input_filepath = path
            self.entry_in.configure(state="normal")
            self.entry_in.delete(0, "end")
            self.entry_in.insert(0, os.path.basename(path))
            self.entry_in.configure(state="disabled")
            self.btn_start.configure(state="normal", fg_color="#007AFF")

    def select_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.settings["output_folder"] = folder
            self.save_settings()
            self.entry_out.configure(state="normal")
            self.entry_out.delete(0, "end")
            self.entry_out.insert(0, folder)
            self.entry_out.configure(state="disabled")

    def start_process(self):
        if not self.input_filepath or not self.settings["output_folder"]: return

        ts = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M")
        base = os.path.splitext(os.path.basename(self.input_filepath))[0]
        fname = f"{base}_DATACOOL_{ts}.xlsx"
        full_output_path = os.path.join(self.settings["output_folder"], fname)

        selected_filter = self.seg_filter.get()

        self.f_success.grid_remove()
        self.btn_start.configure(state="disabled", text="Verarbeite...")

        self.is_processing = True
        self.progress.grid()
        self.progress.set(0)
        self.smooth_progress_loop()

        t = threading.Thread(target=self._run_thread, args=(self.input_filepath, full_output_path, selected_filter))
        t.start()

    def _run_thread(self, in_path, out_path, filter_mode):
        try:
            time.sleep(1.0)
            self.converter.run(in_path, out_path, filter_mode=filter_mode)
            self.final_output_path = out_path
            self.after(0, self._on_success)
        except Exception as e:
            err_msg = str(e)
            self.after(0, lambda: self._on_error(err_msg))

    def _on_success(self):
        self.is_processing = False
        self.progress.set(1)
        self.progress.configure(progress_color="#107C41")

        self.btn_start.configure(text="Erfolgreich! ✅", fg_color="gray")
        self.lbl_status.configure(text="Datei gespeichert.", text_color="green")

        self.f_success.grid()
        self.btn_open.pack(pady=10)

        if not self.log_visible:
            self.geometry("750x630")

        messagebox.showinfo("Erfolg", "Daten erfolgreich konvertiert.")

    def _on_error(self, err_msg):
        self.is_processing = False
        self.progress.grid_remove()
        self.btn_start.configure(state="normal", text="Export Starten", fg_color="#007AFF")
        self.lbl_status.configure(text="Fehler!", text_color="red")

        if not self.log_visible: self.toggle_log()
        messagebox.showerror("Fehler", f"Details:\n{err_msg}")

    def open_excel(self):
        if self.final_output_path:
            try:
                if sys.platform == "win32":
                    os.startfile(self.final_output_path)
                else:
                    # Linux und macOS nutzen andere Befehle
                    opener = "open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, self.final_output_path])
            except Exception as e:
                print(f"Fehler beim Öffnen: {e}")

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()