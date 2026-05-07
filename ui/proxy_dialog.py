from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QLineEdit, QPushButton
)

from proxy.proxy_manager import add_proxy, update_proxy


class ProxyDialog(QDialog):

    def __init__(self, proxy=None):
        super().__init__()

        self.proxy = proxy

        self.setWindowTitle("Proxy")

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Host"))

        self.host = QLineEdit()
        layout.addWidget(self.host)

        layout.addWidget(QLabel("Port"))

        self.port = QLineEdit()
        layout.addWidget(self.port)

        layout.addWidget(QLabel("Username"))

        self.username = QLineEdit()
        layout.addWidget(self.username)

        layout.addWidget(QLabel("Password"))

        self.password = QLineEdit()
        layout.addWidget(self.password)

        btn = QPushButton("Lưu")
        btn.clicked.connect(self.save)

        layout.addWidget(btn)

        self.setLayout(layout)

        if proxy:
            self.host.setText(proxy[1])
            self.port.setText(proxy[2])
            self.username.setText(proxy[3])
            self.password.setText(proxy[4])

    def save(self):

        host = self.host.text()
        port = self.port.text()
        username = self.username.text()
        password = self.password.text()

        if self.proxy:
            update_proxy(self.proxy[0], host, port, username, password)
        else:
            add_proxy(host, port, username, password)

        self.accept()