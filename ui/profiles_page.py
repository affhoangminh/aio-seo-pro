
import threading
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QAbstractItemView, QHeaderView
)
from ui.profile_dialog import ProfileDialog
from profiles.profile_manager import get_profiles, delete_profile
from browser.browser_launcher import launch_browser

class ProfilesPage(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)

        # Toolbar
        toolbar = QHBoxLayout()
        self.btn_add = QPushButton(" ➕ Thêm mới")
        self.btn_add.setObjectName("ActionButton")
        self.btn_edit = QPushButton(" 📝 Sửa")
        self.btn_edit.setObjectName("SecondaryButton")
        self.btn_delete = QPushButton(" 🗑️ Xóa")
        self.btn_delete.setObjectName("DangerButton")
        self.btn_open = QPushButton(" 🚀 Mở Trình duyệt")
        self.btn_open.setObjectName("ActionButton")
        self.btn_select_all = QPushButton(" ✅ Chọn tất cả")
        self.btn_select_all.setObjectName("SecondaryButton")

        self.btn_add.clicked.connect(self.add_profile)
        self.btn_edit.clicked.connect(self.edit_profile)
        self.btn_delete.clicked.connect(self.delete_profile)
        self.btn_open.clicked.connect(lambda: self.open_profiles(bot_mode=False))
        self.btn_select_all.clicked.connect(self.toggle_select_all)

        toolbar.addWidget(self.btn_add)
        toolbar.addWidget(self.btn_edit)
        toolbar.addWidget(self.btn_delete)
        toolbar.addWidget(self.btn_select_all)
        toolbar.addStretch()
        toolbar.addWidget(self.btn_open)
        main_layout.addLayout(toolbar)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["", "ID", "Tên profile", "Proxy", "Trạng thái"])
        self.table.setColumnWidth(0, 40)
        self.table.setColumnWidth(1, 50)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.verticalHeader().setDefaultSectionSize(45)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)
        self.load_profiles()

    def load_profiles(self):
        profiles = get_profiles()
        self.table.setRowCount(0)
        for i, p in enumerate(profiles):
            self.table.insertRow(i)
            proxy_display = f"{p[2]}:{p[3]}" if p[2] and p[3] else "No Proxy"
            chk_item = QTableWidgetItem()
            chk_item.setCheckState(Qt.Unchecked)
            chk_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            self.table.setItem(i, 0, chk_item)
            self.table.setItem(i, 1, QTableWidgetItem(str(p[0])))
            self.table.setItem(i, 2, QTableWidgetItem(p[1]))
            self.table.setItem(i, 3, QTableWidgetItem(proxy_display))
            self.table.setItem(i, 4, QTableWidgetItem("Sẵn sàng"))

    def add_profile(self):
        if ProfileDialog().exec(): self.load_profiles()

    def edit_profile(self):
        row = self.table.currentRow()
        if row >= 0:
            p_id = int(self.table.item(row, 1).text())
            if ProfileDialog((p_id, self.table.item(row, 2).text())).exec():
                self.load_profiles()

    def delete_profile(self):
        row = self.table.currentRow()
        if row >= 0:
            delete_profile(int(self.table.item(row, 1).text()))
            self.load_profiles()

    def open_profiles(self, bot_mode=False):
        for row in range(self.table.rowCount()):
            if self.table.item(row, 0).checkState() == Qt.Checked or self.table.currentRow() == row:
                p_id = int(self.table.item(row, 1).text())
                p_data = next((p for p in get_profiles() if p[0] == p_id), None)
                if p_data:
                    proxy = f"{p_data[2]}:{p_data[3]}:{p_data[4]}:{p_data[5]}" if p_data[2] else None
                    profile = (p_id, p_data[1], proxy, '{"resolution":"1920x1080"}', None)
                    threading.Thread(target=launch_browser, args=(profile, bot_mode), daemon=True).start()

    def toggle_select_all(self):
        any_unchecked = any(self.table.item(r, 0).checkState() == Qt.Unchecked for r in range(self.table.rowCount()))
        state = Qt.Checked if any_unchecked else Qt.Unchecked
        for r in range(self.table.rowCount()): self.table.item(r, 0).setCheckState(state)
        self.btn_select_all.setText(" ❌ Bỏ chọn" if any_unchecked else " ✅ Chọn tất cả")