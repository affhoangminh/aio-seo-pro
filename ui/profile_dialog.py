from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QComboBox
)

from profiles.profile_manager import add_profile, update_profile
from proxy.proxy_manager import get_proxies


class ProfileDialog(QDialog):

    def __init__(self, profile=None):
        super().__init__()

        self.profile = profile

        self.setWindowTitle("Profile")

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

        btn = QPushButton("Lưu")
        btn.clicked.connect(self.save)

        layout.addWidget(btn)

        self.setLayout(layout)

        if profile:
            self.name.setText(profile[1])

    def save(self):

        name = self.name.text()
        proxy_id = self.proxy_combo.currentData()

        if self.profile:
            update_profile(self.profile[0], name, proxy_id)
        else:
            add_profile(name, proxy_id)

        self.accept()