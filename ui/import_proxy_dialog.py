from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QTextEdit, QPushButton
)

from proxy.proxy_manager import add_proxy_bulk


class ImportProxyDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bulk insert proxies")
        self.resize(400, 350)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Định dạng: IP:Port hoặc IP:Port:User:Pass"))

        self.text = QTextEdit()
        layout.addWidget(self.text)

        self.btn_import = QPushButton("Import")
        self.btn_import.clicked.connect(self.import_proxies)

        layout.addWidget(self.btn_import)

        self.setLayout(layout)

    def import_proxies(self):

        lines = self.text.toPlainText().splitlines()

        proxy_list = []

        for line in lines:

            if not line.strip():
                continue

            parts = line.strip().split(":")

            if len(parts) == 2:

                host, port = parts
                proxy_list.append((host, port, "", ""))

            elif len(parts) == 4:

                host, port, user, password = parts
                proxy_list.append((host, port, user, password))

        add_proxy_bulk(proxy_list)

        self.accept()