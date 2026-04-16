import customtkinter as ctk
import frida
import sys
import threading
import os

PACKAGE_NAME = "com.gameparadiso.milkchoco"
LIB_NAME = "libMyGame.so"
INJECT_LIB = "libBypassModule.so"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ASP1RIN PRIVATE")
        self.geometry("400x350")
        ctk.set_appearance_mode("dark")
        
        self.label = ctk.CTkLabel(self, text="ASP1RIN PROJECT", font=("Roboto", 24, "bold"))
        self.label.pack(pady=20)

        self.status_frame = ctk.CTkFrame(self)
        self.status_frame.pack(pady=10, padx=20, fill="x")

        self.status_label = ctk.CTkLabel(self.status_frame, text="Status: Ready", text_color="gray")
        self.status_label.pack(pady=5)

        self.start_button = ctk.CTkButton(self, text="START ENGINE", command=self.start_injection, height=50)
        self.start_button.pack(pady=20)

    def start_injection(self):
        self.start_button.configure(state="disabled")
        threading.Thread(target=self.run_logic, daemon=True).start()

    def run_logic(self):
        try:
            self.status_label.configure(text="Status: Searching Device...", text_color="yellow")
            device = frida.get_usb_device()
            
            self.status_label.configure(text="Status: Spawning Game...", text_color="orange")
            pid = device.spawn([PACKAGE_NAME])
            session = device.attach(pid)
            
            script = session.create_script(self.get_injection_js())
            script.load()
            
            device.resume(pid)
            self.status_label.configure(text="Status: ALL MODULES LOADED", text_color="cyan")
        except Exception as e:
            self.status_label.configure(text="Status: Error", text_color="red")
            self.start_button.configure(state="normal")

    def get_injection_js(self):
        return f"""
        Java.perform(() => {{
            try {{
                const X = Java.use("com.wellbia.xigncode.XigncodeClientSystem");
                X["initialize"].implementation = function (a, b, c, d, e) {{
                    return 0; 
                }};
            }} catch(e) {{}}
        }});

        const libPath = "/data/local/tmp/{INJECT_LIB}"; 
        const dlopen = new NativeFunction(Module.findExportByName(null, "dlopen"), "pointer", ["pointer", "int"]);
        
        var t = setInterval(function() {{
            if (Module.findBaseAddress("{LIB_NAME}")) {{
                clearInterval(t);
                dlopen(Memory.allocUtf8String(libPath), 1);
            }}
        }}, 500);
        """

if __name__ == "__main__":
    app = App()
    app.mainloop()
