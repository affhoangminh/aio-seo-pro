
import json
import os
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, 
    QPushButton, QListWidget, QListWidgetItem, 
    QLabel, QLineEdit, QMessageBox, QInputDialog,
    QComboBox
)
from PySide6.QtCore import Qt, QSize

# Mapping từ Code sang Ngôn ngữ tự nhiên
COMMAND_MAP = {
    "goto": "Truy cập URL",
    "search_google": "Tìm kiếm Google",
    "click_domain": "Tìm & Click Domain",
    "simulate_reading": "Giả lập đọc (Dwell Time)",
    "scroll": "Cuộn trang ngẫu nhiên",
    "click_internal": "Click link nội bộ",
    "mouse_move": "Di chuyển chuột ngẫu nhiên",
    "wait": "Chờ đợi (giây)",
    "bounce": "Giả lập thoát trang (Bounce)"
}

class StepEditorDialog(QDialog):
    def __init__(self, step=None):
        super().__init__()
        self.setWindowTitle("Chỉnh sửa bước")
        self.setMinimumWidth(350)
        self.step = step or {"type": "goto"}

        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Chọn hành động:"))
        self.type_combo = QComboBox()
        for cmd_type, cmd_name in COMMAND_MAP.items():
            self.type_combo.addItem(cmd_name, cmd_type)
        
        # Set current type
        idx = self.type_combo.findData(self.step.get("type"))
        self.type_combo.setCurrentIndex(idx)
        self.type_combo.currentIndexChanged.connect(self.update_fields)
        layout.addWidget(self.type_combo)

        # Dynamic fields
        self.fields_layout = QVBoxLayout()
        layout.addLayout(self.fields_layout)
        self.inputs = {}

        self.update_fields()

        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Xác nhận")
        save_btn.setObjectName("ActionButton")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Hủy")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def update_fields(self):
        # Clear old fields
        while self.fields_layout.count():
            item = self.fields_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.inputs = {}
        cmd_type = self.type_combo.currentData()

        if cmd_type == "goto":
            self.add_field("url", "Địa chỉ URL:", self.step.get("url", "https://"))
        elif cmd_type == "search_google":
            self.add_field("keyword", "Từ khóa tìm kiếm:", self.step.get("keyword", ""))
        elif cmd_type == "click_domain":
            self.add_field("domain", "Tên miền cần tìm (VD: gpm.vn):", self.step.get("domain", ""))
            self.add_field("max_pages", "Tìm tối đa số trang:", str(self.step.get("max_pages", 5)))
        elif cmd_type == "simulate_reading":
            self.add_field("min", "Thời gian tối thiểu (giây):", str(self.step.get("min", 60)))
            self.add_field("max", "Thời gian tối đa (giây):", str(self.step.get("max", 180)))
        elif cmd_type == "click_internal":
            self.add_field("count", "Số lần click link nội bộ:", str(self.step.get("count", 2)))
        elif cmd_type == "wait":
            self.add_field("seconds", "Số giây chờ:", str(self.step.get("seconds", 10)))

    def add_field(self, key, label, value):
        self.fields_layout.addWidget(QLabel(label))
        edit = QLineEdit(value)
        self.fields_layout.addWidget(edit)
        self.inputs[key] = edit

    def get_step(self):
        step = {"type": self.type_combo.currentData()}
        for key, edit in self.inputs.items():
            val = edit.text()
            if val.isdigit():
                val = int(val)
            step[key] = val
        return step

class ScriptEditorDialog(QDialog):
    def __init__(self, file_path=None, file_name=None):
        super().__init__()
        self.file_path = file_path
        self.setWindowTitle("Trình soạn thảo kịch bản SEO")
        self.resize(600, 500)

        layout = QVBoxLayout()
        
        # File Name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Tên kịch bản (ví dụ: seo_google.json):"))
        self.name_edit = QLineEdit(file_name or "new_script.json")
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)

        layout.addWidget(QLabel("Các bước thực hiện (Kéo thả để sắp xếp):"))
        
        self.list_widget = QListWidget()
        self.list_widget.setDragDropMode(QListWidget.InternalMove)
        layout.addWidget(self.list_widget)

        # Step Buttons
        step_btns = QHBoxLayout()
        self.btn_add_step = QPushButton(" ➕ Thêm bước")
        self.btn_add_step.clicked.connect(self.add_step)
        
        self.btn_edit_step = QPushButton(" 📝 Sửa bước")
        self.btn_edit_step.clicked.connect(self.edit_step)
        
        self.btn_remove_step = QPushButton(" 🗑️ Xóa bước")
        self.btn_remove_step.clicked.connect(self.remove_step)
        
        step_btns.addWidget(self.btn_add_step)
        step_btns.addWidget(self.btn_edit_step)
        step_btns.addWidget(self.btn_remove_step)
        layout.addLayout(step_btns)

        # Final Buttons
        final_btns = QHBoxLayout()
        save_btn = QPushButton(" 💾 Lưu kịch bản")
        save_btn.setObjectName("ActionButton")
        save_btn.clicked.connect(self.save_script)
        
        cancel_btn = QPushButton("Hủy")
        cancel_btn.clicked.connect(self.reject)
        
        final_btns.addStretch()
        final_btns.addWidget(save_btn)
        final_btns.addWidget(cancel_btn)
        layout.addLayout(final_btns)

        self.setLayout(layout)

        if self.file_path and os.path.exists(self.file_path):
            self.load_file()

    def load_file(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                steps = json.load(f)
                for step in steps:
                    self.add_step_to_list(step)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể đọc file: {e}")

    def add_step_to_list(self, step):
        cmd_type = step.get("type")
        cmd_name = COMMAND_MAP.get(cmd_type, cmd_type)
        
        # Tạo mô tả tự nhiên
        params = [f"{k}: {v}" for k, v in step.items() if k != "type"]
        desc = f"{cmd_name}"
        if params:
            desc += f" ({', '.join(params)})"
            
        item = QListWidgetItem(desc)
        item.setData(Qt.UserRole, step)
        
        # Thiết lập kích thước cố định cho mỗi dòng để tránh chồng lắp
        current_size = item.sizeHint()
        item.setSizeHint(QSize(current_size.width(), current_size.height() + 30))
        
        self.list_widget.addItem(item)

    def add_step(self):
        dialog = StepEditorDialog()
        if dialog.exec():
            self.add_step_to_list(dialog.get_step())

    def edit_step(self):
        item = self.list_widget.currentItem()
        if not item:
            return
        
        step = item.data(Qt.UserRole)
        dialog = StepEditorDialog(step)
        if dialog.exec():
            new_step = dialog.get_step()
            item.setData(Qt.UserRole, new_step)
            
            # Update text
            cmd_type = new_step.get("type")
            cmd_name = COMMAND_MAP.get(cmd_type, cmd_type)
            params = [f"{k}: {v}" for k, v in new_step.items() if k != "type"]
            desc = f"{cmd_name}"
            if params:
                desc += f" ({', '.join(params)})"
            
            item.setText(desc)

    def remove_step(self):
        item = self.list_widget.currentItem()
        if item:
            self.list_widget.takeItem(self.list_widget.row(item))

    def save_script(self):
        name = self.name_edit.text()
        if not name.endswith(".json"):
            name += ".json"
            
        steps = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            steps.append(item.data(Qt.UserRole))
            
        file_path = os.path.join("scripts", name)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(steps, f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "Thành công", f"Đã lưu kịch bản vào: {file_path}")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể lưu file: {e}")
