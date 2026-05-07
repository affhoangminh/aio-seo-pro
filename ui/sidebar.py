from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton


class Sidebar(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.btn_profiles = QPushButton("Quản lý Profiles")
        self.btn_proxy = QPushButton("Proxy")
        self.btn_settings = QPushButton("Cài đặt")

        layout.addWidget(self.btn_profiles)
        layout.addWidget(self.btn_proxy)
        layout.addWidget(self.btn_settings)

        layout.addStretch()

        self.setLayout(layout)
        self.setFixedWidth(180)