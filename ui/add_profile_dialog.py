from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QLineEdit, QPushButton
)

from profiles.profile_manager import add_profile
from fingerprint.fingerprint_generator import generate_fingerprint


class AddProfileDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Thêm Profile")
        self.setMinimumWidth(300)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Tên profile"))

        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("Proxy"))

        self.proxy_input = QLineEdit()
        layout.addWidget(self.proxy_input)

        self.btn_save = QPushButton("Lưu")
        self.btn_save.clicked.connect(self.save_profile)

        layout.addWidget(self.btn_save)

        self.setLayout(layout)

    def save_profile(self):

        name = self.name_input.text()
        proxy = self.proxy_input.text()

        fingerprint = generate_fingerprint()

        add_profile(name, proxy, fingerprint)

        self.accept()