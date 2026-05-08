from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QComboBox,
    QHBoxLayout, QFileDialog
)

from profiles.profile_manager import add_profile, update_profile, get_profile
from proxy.proxy_manager import get_proxies


class ProfileDialog(QDialog):

    def __init__(self, profile=None):
        super().__init__()

        self.profile = profile

        self.setWindowTitle("Cấu hình Profile")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Tên profile"))

        self.name = QLineEdit()
        layout.addWidget(self.name)

        layout.addWidget(QLabel("Proxy"))

        self.proxy_combo = QComboBox()

        self.proxy_combo.addItem("No Proxy", None)

        proxies = get_proxies()

        for p in proxies:
            proxy_text = f"{p[1]}:{p[2]}"
            self.proxy_combo.addItem(proxy_text, p[0])

        layout.addWidget(self.proxy_combo)

        # Kịch bản SEO
        layout.addWidget(QLabel("Kịch bản Bot (JSON)"))
        script_layout = QHBoxLayout()
        self.script_path = QLineEdit()
        self.btn_browse = QPushButton("Chọn File")
        self.btn_browse.clicked.connect(self.browse_script)
        script_layout.addWidget(self.script_path)
        script_layout.addWidget(self.btn_browse)
        layout.addLayout(script_layout)

        btn = QPushButton("Lưu cấu hình")
        btn.setObjectName("ActionButton")
        btn.clicked.connect(self.save)

        layout.addWidget(btn)

        self.setLayout(layout)

        if profile:
            self.name.setText(profile[1])
            # Load extra data like script_path
            self.load_extra_data(profile[0])

    def load_extra_data(self, profile_id):
        data = get_profile(profile_id)
        if data and len(data) > 6:
            self.script_path.setText(data[6] or "")

    def browse_script(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Chọn kịch bản SEO", "", "JSON Files (*.json)"
        )
        if file_path:
            self.script_path.setText(file_path)

    def save(self):

        name = self.name.text()
        proxy_id = self.proxy_combo.currentData()
        script = self.script_path.text()

        if self.profile:
            update_profile(self.profile[0], name, proxy_id, script)
        else:
            add_profile(name, proxy_id, script_path=script)

        self.accept()