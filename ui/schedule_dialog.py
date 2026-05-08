
import json
import os
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QComboBox, QDateEdit, QTimeEdit, 
    QSpinBox, QPushButton, QListWidget, QListWidgetItem,
    QFileDialog, QMessageBox, QGroupBox, QWidget
)
from PySide6.QtCore import Qt, QDate, QTime
from profiles.profile_manager import get_profiles, add_schedule, update_schedule

class ScheduleDialog(QDialog):
    def __init__(self, schedule_data=None):
        super().__init__()
        self.schedule_data = schedule_data
        self.setWindowTitle("Cấu hình Lịch trình Chiến dịch")
        self.resize(650, 800) # Tăng kích thước cửa sổ một chút
        self.setup_ui()
        if self.schedule_data:
            self.fill_data()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Basic Info
        form_layout = QVBoxLayout()
        lbl_name = QLabel("Tên Lịch trình:")
        lbl_name.setStyleSheet("font-weight: bold; color: #475569;")
        form_layout.addWidget(lbl_name)
        
        self.edit_name = QLineEdit()
        self.edit_name.setPlaceholderText("Ví dụ: Chiến dịch SEO Website A")
        self.edit_name.setMinimumHeight(35)
        form_layout.addWidget(self.edit_name)

        # Profile selection
        lbl_p = QLabel("Chọn Profile thực hiện:")
        lbl_p.setStyleSheet("font-weight: bold; color: #475569; margin-top: 5px;")
        form_layout.addWidget(lbl_p)
        
        self.combo_profile = QComboBox()
        self.combo_profile.setMinimumHeight(35)
        self.combo_profile.addItem("🎲 Ngẫu nhiên (Random)", 0)
        self.combo_profile.addItem("🔄 Dự phòng (Fallback)", -1)
        
        profiles = get_profiles()
        for p in profiles:
            self.combo_profile.addItem(f"👤 {p[1]}", p[0])
        form_layout.addWidget(self.combo_profile)

        # Time Config
        time_group = QGroupBox("📅 Thời gian chạy")
        time_group.setStyleSheet("QGroupBox { font-weight: bold; color: #3b82f6; border: 1px solid #e2e8f0; border-radius: 8px; margin-top: 10px; padding-top: 15px; }")
        time_layout = QHBoxLayout()
        
        v1 = QVBoxLayout()
        v1.addWidget(QLabel("Ngày bắt đầu:"))
        self.date_start = QDateEdit(QDate.currentDate())
        self.date_start.setCalendarPopup(True)
        v1.addWidget(self.date_start)
        
        v2 = QVBoxLayout()
        v2.addWidget(QLabel("Giờ chạy:"))
        self.time_start = QTimeEdit(QTime(10, 30))
        v2.addWidget(self.time_start)
        
        v3 = QVBoxLayout()
        v3.addWidget(QLabel("Số ngày:"))
        self.spin_days = QSpinBox()
        self.spin_days.setRange(1, 365)
        self.spin_days.setValue(30)
        v3.addWidget(self.spin_days)
        
        time_layout.addLayout(v1)
        time_layout.addLayout(v2)
        time_layout.addLayout(v3)
        time_group.setLayout(time_layout)
        form_layout.addWidget(time_group)

        # Scripts sequence
        script_group = QGroupBox("📜 Chuỗi Kịch bản (Sequence)")
        script_group.setStyleSheet("QGroupBox { font-weight: bold; color: #8b5cf6; border: 1px solid #e2e8f0; border-radius: 8px; margin-top: 10px; padding-top: 15px; }")
        script_layout = QVBoxLayout()
        
        h_ctrl = QHBoxLayout()
        self.btn_add_script = QPushButton(" ➕ THÊM SCRIPT ")
        self.btn_add_script.setObjectName("ActionButton")
        self.btn_add_script.setFixedWidth(150)
        self.btn_add_script.clicked.connect(self.add_script_to_list)
        h_ctrl.addWidget(self.btn_add_script)
        h_ctrl.addStretch()
        script_layout.addLayout(h_ctrl)
        
        self.list_scripts = QListWidget()
        self.list_scripts.setSpacing(8)
        self.list_scripts.setSelectionMode(QListWidget.NoSelection)
        self.list_scripts.setStyleSheet("""
            QListWidget { border: none; background: transparent; padding-right: 10px; }
            QListWidget::item { background: transparent; border: none; }
        """)
        script_layout.addWidget(self.list_scripts)
        
        script_group.setLayout(script_layout)
        form_layout.addWidget(script_group)

        # Run Mode
        form_layout.addWidget(QLabel("Chế độ chạy:"))
        self.combo_mode = QComboBox()
        self.combo_mode.setMinimumHeight(35)
        self.combo_mode.addItems(["Traffic Bot", "Better Performance", "Human Simulate"])
        form_layout.addWidget(self.combo_mode)

        layout.addLayout(form_layout)

        # Bottom Buttons
        btn_box = QHBoxLayout()
        self.btn_save = QPushButton(" 💾 LƯU LỊCH TRÌNH ")
        self.btn_save.setObjectName("ActionButton")
        self.btn_save.setMinimumHeight(40)
        self.btn_save.clicked.connect(self.save)
        
        self.btn_cancel = QPushButton(" Hủy ")
        self.btn_cancel.setMinimumHeight(40)
        self.btn_cancel.clicked.connect(self.reject)
        
        btn_box.addStretch()
        btn_box.addWidget(self.btn_cancel)
        btn_box.addWidget(self.btn_save)
        layout.addLayout(btn_box)

        self.setLayout(layout)

    def add_script_to_list(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file kịch bản JSON", "scripts", "JSON Files (*.json)")
        if file_path:
            self.create_script_item(os.path.basename(file_path), file_path, 5)

    def create_script_item(self, name, path, delay):
        item = QListWidgetItem()
        widget = QWidget()
        widget.setMinimumHeight(50)
        widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
            }
        """)
        
        w_layout = QHBoxLayout(widget)
        w_layout.setContentsMargins(15, 0, 15, 0) # Tăng lề trái phải
        w_layout.setSpacing(10)
        
        lbl = QLabel(f"📄 {name}")
        lbl.setStyleSheet("border: none; color: #1e293b; font-size: 12px;")
        w_layout.addWidget(lbl)
        
        w_layout.addStretch()
        
        lbl_delay = QLabel("Nghỉ:")
        lbl_delay.setStyleSheet("border: none; color: #64748b; font-size: 11px;")
        w_layout.addWidget(lbl_delay)
        
        spin = QSpinBox()
        spin.setRange(0, 1440)
        spin.setValue(delay)
        spin.setSuffix("") # Bỏ suffix bên trong
        spin.setFixedWidth(50)
        spin.setStyleSheet("border: 1px solid #cbd5e1; border-radius: 3px; padding: 2px; font-size: 12px;")
        w_layout.addWidget(spin)
        
        lbl_unit = QLabel("Phút")
        lbl_unit.setStyleSheet("border: none; color: #475569; font-size: 11px;")
        w_layout.addWidget(lbl_unit)
        
        # Nút xóa rộng 80px để hiện chữ đầy đủ
        btn_del = QPushButton(" XÓA ")
        btn_del.setFixedWidth(80)
        btn_del.setMinimumHeight(32)
        btn_del.setCursor(Qt.PointingHandCursor)
        btn_del.setStyleSheet("""
            QPushButton {
                border: 1px solid #f87171;
                background-color: #fef2f2;
                color: #ef4444;
                border-radius: 5px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ef4444;
                color: white;
            }
        """)
        btn_del.clicked.connect(lambda: self.remove_item(item))
        w_layout.addWidget(btn_del)
        
        item.setSizeHint(widget.sizeHint())
        item.setData(Qt.UserRole, path)
        item.setData(Qt.UserRole + 1, spin)
        
        self.list_scripts.addItem(item)
        self.list_scripts.setItemWidget(item, widget)

    def remove_item(self, item):
        self.list_scripts.takeItem(self.list_scripts.row(item))

    def fill_data(self):
        self.edit_name.setText(self.schedule_data[1])
        index = self.combo_profile.findData(self.schedule_data[2])
        if index >= 0: self.combo_profile.setCurrentIndex(index)
        self.date_start.setDate(QDate.fromString(self.schedule_data[3], "yyyy-MM-dd"))
        self.time_start.setTime(QTime.fromString(self.schedule_data[4], "HH:mm"))
        self.spin_days.setValue(self.schedule_data[5])
        scripts = json.loads(self.schedule_data[7])
        for s in scripts:
            self.create_script_item(os.path.basename(s['path']), s['path'], s['delay'])
        self.combo_mode.setCurrentText(self.schedule_data[8])

    def save(self):
        name = self.edit_name.text()
        if not name:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên lịch trình!")
            return
        profile_id = self.combo_profile.currentData()
        start_date = self.date_start.date().toString("yyyy-MM-dd")
        start_time = self.time_start.time().toString("HH:mm")
        duration = self.spin_days.value()
        run_mode = self.combo_mode.currentText()
        scripts = []
        for i in range(self.list_scripts.count()):
            item = self.list_scripts.item(i)
            path = item.data(Qt.UserRole)
            spin = item.data(Qt.UserRole + 1)
            scripts.append({"path": path, "delay": spin.value()})
        scripts_json = json.dumps(scripts)
        if self.schedule_data:
            update_schedule(self.schedule_data[0], name, profile_id, start_date, start_time, duration, scripts_json, run_mode)
        else:
            add_schedule(name, profile_id, start_date, start_time, duration, scripts_json, run_mode)
        self.accept()
