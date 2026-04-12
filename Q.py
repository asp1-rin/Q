import sys
import math
import time
import threading
import frida
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

PROCESS_NAME = "com.gameparadiso.milkchoco"
LIB_NAME = "libMyGame.so"
BYPASS_OFF = 0x182ec
AOB_SIG = "2D E9 F0 4F 8B 46 00 20"

class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.WindowTransparentForInput)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        rect = QApplication.primaryScreen().geometry()
        self.setGeometry(0, 0, rect.width(), rect.height())
        self.cx, self.cy = rect.width() // 2, rect.height() // 2
        self.radius = 100
        self.active = False

    def paintEvent(self, event):
        if not self.active: return
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(QPen(QColor(0, 255, 0, 160), 2))
        p.drawEllipse(QPoint(self.cx, self.cy), self.radius, self.radius)
        p.drawLine(self.cx - 8, self.cy, self.cx + 8, self.cy)
        p.drawLine(self.cx, self.cy - 8, self.cx, self.cy + 8)

class QAdmin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.ovl = Overlay()
        self.session = None

    def init_ui(self):
        self.setWindowTitle("Q-Analyzer Pro")
        self.setFixedSize(400, 550)
        self.setStyleSheet("background-color: #111; color: #eee;")
        
        main_layout = QVBoxLayout()
        self.st_lbl = QLabel("READY")
        self.st_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.st_lbl)

        main_layout.addWidget(QLabel("FOV Range"))
        self.sld = QSlider(Qt.Orientation.Horizontal)
        self.sld.setRange(50, 500)
        self.sld.setValue(100)
        self.sld.valueChanged.connect(self.sync_fov)
        main_layout.addWidget(self.sld)

        self.run_btn = QPushButton("LAUNCH ENGINE")
        self.run_btn.setFixedHeight(60)
        self.run_btn.setStyleSheet("background-color: #900; font-weight: bold; border-radius: 5px;")
        self.run_btn.clicked.connect(self.start)
        main_layout.addWidget(self.run_btn)

        self.log_v = QTextEdit()
        self.log_v.setReadOnly(True)
        self.log_v.setStyleSheet("background-color: #000; color: #0f0; font-family: Consolas;")
        main_layout.addWidget(self.log_v)

        w = QWidget()
        w.setLayout(main_layout)
        self.setCentralWidget(w)

    def sync_fov(self, v):
        self.ovl.radius = v
        self.ovl.update()

    def log(self, m):
        self.log_v.append(f"[{time.strftime('%H:%M:%S')}] {m}")

    def start(self):
        self.ovl.active = True
        self.ovl.show()
        threading.Thread(target=self.core, daemon=True).start()

    def core(self):
        try:
            dev = frida.get_usb_device()
            pid = dev.spawn([PROCESS_NAME])
            self.session = dev.attach(pid)
            
            payload = f"""
            var b = Module.findBaseAddress("libxigncode.so");
            if(b) {{
                Interceptor.attach(b.add({BYPASS_OFF}), {{
                    onLeave: function(r) {{ r.replace(0); }}
                }});
                send("Bypass Active");
            }}
            var m = Module.findModuleByName("{LIB_NAME}");
            if(m) {{
                var s = Memory.scanSync(m.base, m.size, "{AOB_SIG}");
                if(s.length > 0) {{
                    send("Aim Logic Synced: " + s[0].address);
                }}
            }}
            """
            sc = self.session.create_script(payload)
            sc.on('message', lambda msg, data: self.log(msg['payload']))
            sc.load()
            dev.resume(pid)
            self.st_lbl.setText("ACTIVE")
            self.st_lbl.setStyleSheet("color: #0f0;")
        except Exception as e:
            self.log(str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = QAdmin()
    ex.show()
    sys.exit(app.exec())
