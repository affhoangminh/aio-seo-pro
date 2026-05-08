
import os
import json
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QFileDialog
)
from PySide6.QtCore import Qt
from ui.script_editor_dialog import ScriptEditorDialog

class ScriptManagerPage(QWidget):
    def __init__(self):
        super().__init__()
        self.script_dir = "scripts"
        os.makedirs(self.script_dir, exist_ok=True)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        self.btn_new = QPushButton(" ➕ Tạo kịch bản mới")
        self.btn_new.setObjectName("ActionButton")
        self.btn_new.clicked.connect(self.new_script)

        self.btn_edit = QPushButton(" 📝 Sửa")
        self.btn_edit.setObjectName("SecondaryButton")
        self.btn_edit.clicked.connect(self.edit_script)

        self.btn_delete = QPushButton(" 🗑️ Xóa")
        self.btn_delete.setObjectName("DangerButton")
        self.btn_delete.clicked.connect(self.delete_script)

        toolbar.addWidget(self.btn_new)
        toolbar.addWidget(self.btn_edit)
        toolbar.addStretch()
        toolbar.addWidget(self.btn_delete)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Tên kịch bản", "Đường dẫn"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)

        layout.addLayout(toolbar)
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.load_scripts()

    def load_scripts(self):
        self.table.setRowCount(0)
        if not os.path.exists(self.script_dir):
            return

        files = [f for f in os.listdir(self.script_dir) if f.endswith(".json")]
        for i, file in enumerate(files):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(file))
            self.table.setItem(i, 1, QTableWidgetItem(os.path.abspath(os.path.join(self.script_dir, file))))

    def new_script(self):
        dialog = ScriptEditorDialog()
        if dialog.exec():
            self.load_scripts()

    def edit_script(self):
        row = self.table.currentRow()
        if row < 0:
            return
        
        file_name = self.table.item(row, 0).text()
        file_path = self.table.item(row, 1).text()
        
        dialog = ScriptEditorDialog(file_path, file_name)
        if dialog.exec():
            self.load_scripts()

    def delete_script(self):
        row = self.table.currentRow()
        if row < 0:
            return
        
        file_name = self.table.item(row, 0).text()
        file_path = self.table.item(row, 1).text()
        
        reply = QMessageBox.question(self, "Xác nhận", f"Bạn có chắc muốn xóa kịch bản '{file_name}'?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                os.remove(file_path)
                self.load_scripts()
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể xóa file: {e}")
