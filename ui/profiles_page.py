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

        # =========================
        # TOOLBAR
        # =========================

        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        self.btn_add = QPushButton(" ➕ Thêm mới")
        self.btn_add.setObjectName("ActionButton")
        
        self.btn_import = QPushButton(" 📥 Import")
        self.btn_import.setObjectName("SecondaryButton")
        
        self.btn_edit = QPushButton(" 📝 Sửa")
        self.btn_edit.setObjectName("SecondaryButton")
        
        self.btn_delete = QPushButton(" 🗑️ Xóa")
        self.btn_delete.setObjectName("DangerButton")
        
        self.btn_open = QPushButton(" 🚀 Mở")
        self.btn_open.setObjectName("ActionButton")
        
        self.btn_run_bot = QPushButton(" 🤖 Chạy Traffic Bot")
        self.btn_run_bot.setObjectName("ActionButton")
        self.btn_run_bot.setStyleSheet("background-color: #8b5cf6;") # Custom purple for bot

        self.btn_select_all = QPushButton(" ✅ Chọn tất cả")
        self.btn_select_all.setObjectName("SecondaryButton")

        self.btn_add.clicked.connect(self.add_profile)
        self.btn_edit.clicked.connect(self.edit_profile)
        self.btn_delete.clicked.connect(self.delete_profile)
        self.btn_open.clicked.connect(lambda: self.open_profiles(bot_mode=False))
        self.btn_run_bot.clicked.connect(lambda: self.open_profiles(bot_mode=True))
        self.btn_select_all.clicked.connect(self.toggle_select_all)

        toolbar.addWidget(self.btn_add)
        toolbar.addWidget(self.btn_import)
        toolbar.addWidget(self.btn_edit)
        toolbar.addWidget(self.btn_delete)
        toolbar.addWidget(self.btn_select_all)
        toolbar.addStretch()
        toolbar.addWidget(self.btn_open)
        toolbar.addWidget(self.btn_run_bot)


        # =========================
        # TABLE
        # =========================

        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)

        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "",
            "ID",
            "Tên profile",
            "Proxy",
            "Kịch bản Bot",
            "Trạng thái"
        ])


        # Column widths
        self.table.setColumnWidth(0, 40)
        self.table.setColumnWidth(1, 50)
        self.table.setColumnWidth(2, 180)
        self.table.setColumnWidth(3, 180)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)

        # Selection behavior
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setDefaultSectionSize(45) # Tăng chiều cao dòng cho chuyên nghiệp


        # Events
        self.table.cellDoubleClicked.connect(self.on_double_click)

        main_layout.addLayout(toolbar)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

        self.load_profiles()

    # =========================
    # DOUBLE CLICK EVENT
    # =========================

    def on_double_click(self, row, column):
        self.open_single_profile(row, bot_mode=False)

    # =========================
    # LOAD PROFILES
    # =========================

    def load_profiles(self):

        profiles = get_profiles()

        self.table.setRowCount(0)

        for i, p in enumerate(profiles):

            self.table.insertRow(i)

            profile_id = p[0]
            name = p[1]

            host = p[2]
            port = p[3]

            proxy_display = "No Proxy"

            if host and port:
                proxy_display = f"{host}:{port}"

            script_path = p[6] if len(p) > 6 else None
            script_display = "---"
            if script_path:
                import os
                script_display = os.path.basename(script_path)

            # Checkbox item
            chk_item = QTableWidgetItem()
            chk_item.setCheckState(Qt.Unchecked)
            chk_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            
            self.table.setItem(i, 0, chk_item)
            self.table.setItem(i, 1, QTableWidgetItem(str(profile_id)))
            self.table.setItem(i, 2, QTableWidgetItem(name))
            self.table.setItem(i, 3, QTableWidgetItem(proxy_display))
            
            # Script Item (Highlight)
            script_item = QTableWidgetItem(script_display)
            if script_path:
                script_item.setForeground(Qt.blue)
            self.table.setItem(i, 4, script_item)
            
            self.table.setItem(i, 5, QTableWidgetItem("Sẵn sàng"))


    # =========================
    # ADD PROFILE
    # =========================

    def add_profile(self):

        dialog = ProfileDialog()

        if dialog.exec():
            self.load_profiles()

    # =========================
    # EDIT PROFILE
    # =========================

    def edit_profile(self):

        row = self.table.currentRow()

        if row < 0:
            return

        profile = (
            int(self.table.item(row, 1).text()),
            self.table.item(row, 2).text()
        )

        dialog = ProfileDialog(profile)

        if dialog.exec():
            self.load_profiles()

    # =========================
    # DELETE PROFILE
    # =========================

    def delete_profile(self):

        row = self.table.currentRow()

        if row < 0:
            return

        profile_id = int(self.table.item(row, 1).text())

        delete_profile(profile_id)

        self.load_profiles()

    # =========================
    # OPEN SINGLE PROFILE
    # =========================

    def open_single_profile(self, row, bot_mode=False):
        
        profile_id = int(self.table.item(row, 1).text())
        name = self.table.item(row, 2).text()
        
        profiles = get_profiles()
        proxy_string = None
        script_path = None

        for p in profiles:
            if p[0] == profile_id:
                host = p[2]
                port = p[3]
                username = p[4]
                password = p[5]
                script_path = p[6] if len(p) > 6 else None
                
                if host and port:
                    if username and password:
                        proxy_string = f"{host}:{port}:{username}:{password}"
                    else:
                        proxy_string = f"{host}:{port}"

        profile = (
            profile_id,
            name,
            proxy_string,
            '{"user_agent":"Mozilla/5.0","resolution":"1920x1080"}',
            script_path
        )

        from browser.browser_worker import add_task
        add_task(launch_browser, profile, bot_mode)


    # =========================
    # OPEN MULTIPLE PROFILES
    # =========================

    def open_profiles(self, bot_mode=False):

        checked_profiles = []
        for row in range(self.table.rowCount()):
            if self.table.item(row, 0).checkState() == Qt.Checked:
                checked_profiles.append(row)

        # Nếu không chọn checkbox nào thì lấy row đang được chọn (highlight)
        if not checked_profiles:
            row = self.table.currentRow()
            if row >= 0:
                checked_profiles.append(row)

        if not checked_profiles:
            return

        for row in checked_profiles:
            self.open_single_profile(row, bot_mode)

    # =========================
    # TOGGLE SELECT ALL
    # =========================

    def toggle_select_all(self):
        # Kiểm tra xem có ô nào chưa được chọn không
        any_unchecked = False
        for row in range(self.table.rowCount()):
            if self.table.item(row, 0).checkState() == Qt.Unchecked:
                any_unchecked = True
                break
        
        target_state = Qt.Checked if any_unchecked else Qt.Unchecked
        
        for row in range(self.table.rowCount()):
            self.table.item(row, 0).setCheckState(target_state)
        
        # Đổi text nút cho trực quan
        if target_state == Qt.Checked:
            self.btn_select_all.setText(" ❌ Bỏ chọn tất cả")
        else:
            self.btn_select_all.setText(" ✅ Chọn tất cả")