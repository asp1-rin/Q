import customtkinter as ctk
import frida
import threading
import os
import sys
from overlay import GameOverlay

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ASP1RIN PRIVATE")
        self.geometry("400x550")
        ctk.set_appearance_mode("dark")
        
        icon_path = resource_path("assets/Q.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        self.ov = GameOverlay()
        
        ctk.CTkLabel(self, text="AIM SETTINGS", font=("Roboto", 16, "bold")).pack(pady=15)
        
        self.smooth_slider = ctk.CTkSlider(self, from_=0.01, to=1.0, command=self.update_aim_params)
        self.smooth_slider.set(0.5)
        self.smooth_slider.pack(pady=5)
        ctk.CTkLabel(self, text="Aim Smooth").pack()

        self.fov_slider = ctk.CTkSlider(self, from_=50, to=500, command=self.update_aim_params)
        self.fov_slider.set(150)
        self.fov_slider.pack(pady=5)
        ctk.CTkLabel(self, text="FOV Size").pack()

        self.recoil_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(self, text="No Recoil", variable=self.recoil_var, command=self.toggle_weapon).pack(pady=10)

        self.spread_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(self, text="No Spread", variable=self.spread_var, command=self.toggle_weapon).pack(pady=10)

        self.start_btn = ctk.CTkButton(self, text="START ENGINE", command=self.start_injection, height=50)
        self.start_btn.pack(pady=30)
        
        self.script = None

    def update_aim_params(self, _=None):
        if self.script:
            smooth = self.smooth_slider.get()
            fov = self.fov_slider.get()
            self.ov.fov_radius = fov
            self.script.runtime.enqueue_job(f"Aimbot.smooth = {smooth}; Aimbot.fovSize = {fov};")

    def toggle_weapon(self):
        if self.script:
            recoil = str(self.recoil_var.get()).lower()
            spread = str(self.spread_var.get()).lower()
            self.script.runtime.enqueue_job(f"Weapon.setNoRecoil({recoil}); Weapon.setNoSpread({spread});")

    def on_message(self, message, data):
        if message['type'] == 'send' and message['payload']['type'] == 'esp_data':
            self.ov.draw_esp(message['payload']['data'])

    def start_injection(self):
        threading.Thread(target=self.run_logic, daemon=True).start()
        threading.Thread(target=self.run_overlay, daemon=True).start()

    def run_logic(self):
        try:
            device = frida.get_usb_device()
            session = device.attach("com.gameparadiso.milkchoco")
            
            scripts = ["offsets.js", "bypass.js", "weapon.js", "esp.js", "aimbot.js"]
            combined = ""
            base_path = resource_path("engine")
            
            for s in scripts:
                with open(os.path.join(base_path, s), "r", encoding='utf-8') as f:
                    combined += f.read() + "\n"
            
            self.script = session.create_script(combined)
            self.script.on('message', self.on_message)
            self.script.load()
        except:
            pass

    def run_overlay(self):
        while True:
            self.ov.update_overlay()

if __name__ == "__main__":
    app = App()
    app.mainloop()
