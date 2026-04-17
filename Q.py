import customtkinter as ctk
import frida
import threading
import os
from overlay import GameOverlay

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ASP1RIN PRIVATE")
        self.geometry("400x550")
        
        self.ov = GameOverlay()
        
        ctk.CTkLabel(self, text="AIM SETTINGS", font=("Roboto", 16)).pack(pady=10)
        
        self.smooth_slider = ctk.CTkSlider(self, from_=0.01, to=1.0, command=self.update_aim_params)
        self.smooth_slider.set(0.5)
        self.smooth_slider.pack(pady=5)
        ctk.CTkLabel(self, text="Aim Smooth").pack()

        self.fov_slider = ctk.CTkSlider(self, from_=50, to=500, command=self.update_aim_params)
        self.fov_slider.set(150)
        self.fov_slider.pack(pady=5)
        ctk.CTkLabel(self, text="FOV Size").pack()

        self.start_btn = ctk.CTkButton(self, text="START ENGINE", command=self.start_injection)
        self.start_btn.pack(pady=30)
        
        self.script = None

    def update_aim_params(self, _=None):
        if self.script:
            smooth = self.smooth_slider.get()
            fov = self.fov_slider.get()
            self.ov.fov_radius = fov
            self.script.runtime.enqueue_job(f"Aimbot.smooth = {smooth}; Aimbot.fovSize = {fov};")

    def on_message(self, message, data):
        if message['type'] == 'send' and message['payload']['type'] == 'esp_data':
            self.ov.draw_esp(message['payload']['data'])

    def start_injection(self):
        threading.Thread(target=self.run_logic, daemon=True).start()
        threading.Thread(target=self.run_overlay, daemon=True).start()

    def run_logic(self):
        device = frida.get_usb_device()
        session = device.attach("com.gameparadiso.milkchoco")
        
        scripts = ["offsets.js", "bypass.js", "weapon.js", "esp.js", "aimbot.js"]
        combined = ""
        for s in scripts:
            with open(f"engine/{s}", "r", encoding='utf-8') as f:
                combined += f.read() + "\n"
        
        self.script = session.create_script(combined)
        self.script.on('message', self.on_message)
        self.script.load()

    def run_overlay(self):
        while True:
            self.ov.update_overlay()

if __name__ == "__main__":
    app = App()
    app.mainloop()
