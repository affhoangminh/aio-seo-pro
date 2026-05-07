from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem
)

from ui.proxy_dialog import ProxyDialog
from ui.import_proxy_dialog import ImportProxyDialog
from proxy.proxy_manager import get_proxies, delete_proxy
from proxy.proxy_checker import check_proxy_list


class ProxyPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # toolbar
        toolbar = QHBoxLayout()

        self.btn_add = QPushButton("Thêm")
        self.btn_import = QPushButton("Import")
        self.btn_edit = QPushButton("Sửa")
        self.btn_check = QPushButton("Check Proxy")
        self.btn_delete = QPushButton("Xóa")

        toolbar.addWidget(self.btn_add)
        toolbar.addWidget(self.btn_import)
        toolbar.addWidget(self.btn_edit)
        toolbar.addWidget(self.btn_check)
        toolbar.addWidget(self.btn_delete)
        toolbar.addStretch()

        # table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["ID","Host","Port","User","Password","Status","Speed"]
        )

        layout.addLayout(toolbar)
        layout.addWidget(self.table)

        self.setLayout(layout)

        # events
        self.btn_add.clicked.connect(self.add_proxy)
        self.btn_import.clicked.connect(self.import_proxy)
        self.btn_edit.clicked.connect(self.edit_proxy)
        self.btn_check.clicked.connect(self.check_proxies)
        self.btn_delete.clicked.connect(self.delete_proxy)

        self.load_proxies()

    def load_proxies(self):

        proxies = get_proxies()

        self.table.setRowCount(0)
        self.table.setRowCount(len(proxies))

        for i, p in enumerate(proxies):

            for j in range(5):
                self.table.setItem(i, j, QTableWidgetItem(str(p[j])))

    def add_proxy(self):

        dialog = ProxyDialog()

        if dialog.exec():
            self.load_proxies()

    def edit_proxy(self):

        row = self.table.currentRow()

        if row < 0:
            return

        proxy = (
            int(self.table.item(row, 0).text()),
            self.table.item(row, 1).text(),
            self.table.item(row, 2).text(),
            self.table.item(row, 3).text(),
            self.table.item(row, 4).text()
        )

        dialog = ProxyDialog(proxy)

        if dialog.exec():
            self.load_proxies()

    def delete_proxy(self):

        row = self.table.currentRow()

        if row < 0:
            return

        proxy_id = int(self.table.item(row, 0).text())

        delete_proxy(proxy_id)

        self.load_proxies()

    def import_proxy(self):

        dialog = ImportProxyDialog()

        if dialog.exec():
            self.load_proxies()

    def check_proxies(self):

        proxies = get_proxies()

        def update(proxy, status, speed):

            proxy_id = proxy[0]

            for row in range(self.table.rowCount()):

                if int(self.table.item(row,0).text()) == proxy_id:

                    self.table.setItem(row,5,QTableWidgetItem(status))
                    self.table.setItem(row,6,QTableWidgetItem(str(speed)))

        check_proxy_list(proxies, update)