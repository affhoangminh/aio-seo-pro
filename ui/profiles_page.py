import threading

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QAbstractItemView
)

from ui.profile_dialog import ProfileDialog

from profiles.profile_manager import get_profiles, delete_profile

from browser.browser_launcher import launch_browser


class ProfilesPage(QWidget):

    def __init__(self):

        super().__init__()

        main_layout = QVBoxLayout()

        # =========================
        # TOOLBAR
        # =========================

        toolbar = QHBoxLayout()

        self.btn_add = QPushButton("Thêm mới")
        self.btn_import = QPushButton("Import")
        self.btn_edit = QPushButton("Sửa")
        self.btn_delete = QPushButton("Xóa")
        self.btn_open = QPushButton("Mở")

        self.btn_add.clicked.connect(self.add_profile)
        self.btn_edit.clicked.connect(self.edit_profile)
        self.btn_delete.clicked.connect(self.delete_profile)
        self.btn_open.clicked.connect(self.open_profiles)

        toolbar.addWidget(self.btn_add)
        toolbar.addWidget(self.btn_import)
        toolbar.addWidget(self.btn_edit)
        toolbar.addWidget(self.btn_delete)
        toolbar.addWidget(self.btn_open)
        toolbar.addStretch()

        # =========================
        # TABLE
        # =========================

        self.table = QTableWidget()

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Tên profile",
            "Proxy",
            "Trạng thái"
        ])

        # cho phép chọn nhiều profile
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.MultiSelection)

        main_layout.addLayout(toolbar)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

        self.load_profiles()

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

            self.table.setItem(i, 0, QTableWidgetItem(str(profile_id)))
            self.table.setItem(i, 1, QTableWidgetItem(name))
            self.table.setItem(i, 2, QTableWidgetItem(proxy_display))
            self.table.setItem(i, 3, QTableWidgetItem("Sẵn sàng"))

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
            int(self.table.item(row, 0).text()),
            self.table.item(row, 1).text()
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

        profile_id = int(self.table.item(row, 0).text())

        delete_profile(profile_id)

        self.load_profiles()

    # =========================
    # OPEN MULTIPLE PROFILES
    # =========================

    def open_profiles(self):

        selected_rows = self.table.selectionModel().selectedRows()

        if not selected_rows:
            return

        profiles = get_profiles()

        for row_index in selected_rows:

            row = row_index.row()

            profile_id = int(self.table.item(row, 0).text())
            name = self.table.item(row, 1).text()

            proxy_string = None

            for p in profiles:

                if p[0] == profile_id:

                    host = p[2]
                    port = p[3]
                    username = p[4]
                    password = p[5]

                    if host and port:

                        if username and password:
                            proxy_string = f"{host}:{port}:{username}:{password}"
                        else:
                            proxy_string = f"{host}:{port}"

            profile = (
                profile_id,
                name,
                proxy_string,
                '{"user_agent":"Mozilla/5.0","resolution":"1920x1080"}'
            )

            from browser.browser_worker import add_task

            add_task(launch_browser, profile)