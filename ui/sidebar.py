from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt


class Sidebar(QWidget):

    def __init__(self):
        super().__init__()
        self.setObjectName("Sidebar")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Brand Logo / Title
        self.brand_label = QLabel("AIO SEO PRO")
        self.brand_label.setObjectName("SidebarLabel")
        self.brand_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.brand_label)

        # Menu Buttons
        self.btn_profiles = QPushButton(" 👤 Profiles")
        self.btn_proxy = QPushButton(" 🌐 Proxy")
        self.btn_scripts = QPushButton(" 📜 Quản lý Kịch bản")
        self.btn_schedule = QPushButton(" 📅 Lịch trình")
        self.btn_settings = QPushButton(" ⚙️ Cài đặt")

        # Set IDs for styling
        self.btn_profiles.setProperty("active", "true")

        layout.addWidget(self.btn_profiles)
        layout.addWidget(self.btn_proxy)
        layout.addWidget(self.btn_scripts)
        layout.addWidget(self.btn_schedule)
        layout.addWidget(self.btn_settings)

        layout.addStretch()

        # Footer version
        version_label = QLabel("v2.1.0")
        version_label.setStyleSheet("color: #475569; padding: 10px; font-size: 10px;")
        version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(version_label)

        self.setLayout(layout)
        self.setFixedWidth(220)

    def set_active(self, btn):
        # Reset all
        self.btn_profiles.setProperty("active", "false")
        self.btn_proxy.setProperty("active", "false")
        self.btn_scripts.setProperty("active", "false")
        self.btn_schedule.setProperty("active", "false")
        self.btn_settings.setProperty("active", "false")

        
        # Set active
        btn.setProperty("active", "true")
        
        # Refresh style
        self.btn_profiles.style().unpolish(self.btn_profiles)
        self.btn_profiles.style().polish(self.btn_profiles)
        self.btn_proxy.style().unpolish(self.btn_proxy)
        self.btn_proxy.style().polish(self.btn_proxy)
        self.btn_scripts.style().unpolish(self.btn_scripts)
        self.btn_scripts.style().polish(self.btn_scripts)
        self.btn_schedule.style().unpolish(self.btn_schedule)
        self.btn_schedule.style().polish(self.btn_schedule)
        self.btn_settings.style().unpolish(self.btn_settings)
        self.btn_settings.style().polish(self.btn_settings)