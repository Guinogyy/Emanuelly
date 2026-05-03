import tkinter as tk
from tkinter import ttk
import threading
import time
import mss
import pytesseract
from deep_translator import GoogleTranslator
from PIL import Image
import os

class ScreenTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Translator Setup")
        self.root.geometry("400x300")

        self.running = False
        self.overlay_window = None
        self.process_thread = None

        self.sct = mss.mss()
        # Default capture region (can be adjusted)
        self.capture_region = {"left": 0, "top": 0, "width": 800, "height": 200}

        self.setup_ui()

    def setup_ui(self):
        # Settings frame
        settings_frame = ttk.LabelFrame(self.root, text="Settings")
        settings_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Region selection
        ttk.Label(settings_frame, text="X:").grid(row=0, column=0, padx=5, pady=5)
        self.x_var = tk.StringVar(value=str(self.capture_region["left"]))
        ttk.Entry(settings_frame, textvariable=self.x_var, width=5).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(settings_frame, text="Y:").grid(row=0, column=2, padx=5, pady=5)
        self.y_var = tk.StringVar(value=str(self.capture_region["top"]))
        ttk.Entry(settings_frame, textvariable=self.y_var, width=5).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(settings_frame, text="Width:").grid(row=1, column=0, padx=5, pady=5)
        self.w_var = tk.StringVar(value=str(self.capture_region["width"]))
        ttk.Entry(settings_frame, textvariable=self.w_var, width=5).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(settings_frame, text="Height:").grid(row=1, column=2, padx=5, pady=5)
        self.h_var = tk.StringVar(value=str(self.capture_region["height"]))
        ttk.Entry(settings_frame, textvariable=self.h_var, width=5).grid(row=1, column=3, padx=5, pady=5)

        # Source language
        ttk.Label(settings_frame, text="Source Language:").grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        self.source_lang_var = tk.StringVar(value="auto")
        ttk.Entry(settings_frame, textvariable=self.source_lang_var, width=10).grid(row=2, column=2, columnspan=2, padx=5, pady=5, sticky="w")

        # Target language
        ttk.Label(settings_frame, text="Target Language:").grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        self.target_lang_var = tk.StringVar(value="pt")
        ttk.Entry(settings_frame, textvariable=self.target_lang_var, width=10).grid(row=3, column=2, columnspan=2, padx=5, pady=5, sticky="w")

        # Start/Stop Button
        self.toggle_btn = ttk.Button(self.root, text="Start Translation", command=self.toggle_translation)
        self.toggle_btn.pack(pady=10)

    def update_capture_region(self):
        try:
            self.capture_region = {
                "left": int(self.x_var.get()),
                "top": int(self.y_var.get()),
                "width": int(self.w_var.get()),
                "height": int(self.h_var.get())
            }
        except ValueError:
            print("Invalid capture region values")

    def toggle_translation(self):
        if self.running:
            self.stop_translation()
        else:
            self.start_translation()

    def start_translation(self):
        self.update_capture_region()
        self.running = True
        self.toggle_btn.config(text="Stop Translation")

        # Create overlay
        self.create_overlay()

        # Start processing thread
        self.process_thread = threading.Thread(target=self.process_screen)
        self.process_thread.daemon = True
        self.process_thread.start()

    def stop_translation(self):
        self.running = False
        self.toggle_btn.config(text="Start Translation")

        if self.overlay_window:
            self.overlay_window.destroy()
            self.overlay_window = None

    def create_overlay(self):
        self.overlay_window = tk.Toplevel(self.root)
        self.overlay_window.title("Translation Overlay")
        self.overlay_window.attributes("-topmost", True)
        self.overlay_window.attributes("-alpha", 0.8)
        self.overlay_window.configure(bg='black')

        # Position the overlay slightly below the capture region
        overlay_y = self.capture_region["top"] + self.capture_region["height"] + 10
        self.overlay_window.geometry(f"600x150+{self.capture_region['left']}+{overlay_y}")
        self.overlay_window.overrideredirect(True) # Remove window borders

        self.text_label = tk.Label(self.overlay_window, text="Waiting for text...", font=("Arial", 16), fg="white", bg="black", wraplength=580, justify="left")
        self.text_label.pack(expand=True, fill="both", padx=10, pady=10)

        # Bind events to move overlay
        self.overlay_window.bind("<ButtonPress-1>", self.start_move)
        self.overlay_window.bind("<B1-Motion>", self.on_motion)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def on_motion(self, event):
        if not self.overlay_window:
            return
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.overlay_window.winfo_x() + deltax
        y = self.overlay_window.winfo_y() + deltay
        self.overlay_window.geometry(f"+{x}+{y}")

    def process_screen(self):
        translator = GoogleTranslator(source=self.source_lang_var.get(), target=self.target_lang_var.get())
        last_text = ""

        while self.running:
            try:
                # Capture screen
                sct_img = self.sct.grab(self.capture_region)
                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

                # OCR
                text = pytesseract.image_to_string(img).strip()

                # If we found new text, translate it
                if text and text != last_text and len(text) > 2:
                    last_text = text
                    translated = translator.translate(text)
                    self.update_overlay_label(f"Original: {text}\n\nPT: {translated}")

            except Exception as e:
                print(f"Error processing screen: {e}")

            # Sleep to reduce CPU usage
            time.sleep(1)

    def update_overlay_label(self, text):
        if self.running and self.overlay_window:
            self.overlay_window.after(0, lambda: self.text_label.config(text=text))

if __name__ == "__main__":
    if os.environ.get('DISPLAY') is None:
        print("Warning: DISPLAY environment variable is not set. GUI may not launch in headless environment.")
        # We handle this gracefully here for testing purposes
        try:
            root = tk.Tk()
            app = ScreenTranslatorApp(root)

            # Handle window close event
            def on_closing():
                app.stop_translation()
                root.destroy()

            root.protocol("WM_DELETE_WINDOW", on_closing)
            root.mainloop()
        except Exception as e:
            print(f"Failed to start GUI: {e}")
    else:
        root = tk.Tk()
        app = ScreenTranslatorApp(root)

        # Handle window close event
        def on_closing():
            app.stop_translation()
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
