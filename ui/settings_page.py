
import json
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox,
    QCheckBox, QTimeEdit, QSpinBox, QGroupBox
)
from PySide6.QtCore import QTime

CONFIG_FILE = "database/config.json"

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.load_config()

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("⚙️ Cấu hình Hệ thống & Lập lịch")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #1e293b;")
        layout.addWidget(title)

        # 1. Captcha Section
        captcha_group = QGroupBox("Cấu hình Giải CAPTCHA tự động")
        captcha_layout = QVBoxLayout()
        
        service_layout = QHBoxLayout()
        service_layout.addWidget(QLabel("Dịch vụ sử dụng:"))
        self.service_combo = QComboBox()
        self.service_combo.addItems(["Anti-Captcha", "2Captcha", "CapMonster"])
        self.service_combo.setCurrentText(self.config.get("captcha_service", "Anti-Captcha"))
        service_layout.addWidget(self.service_combo)
        captcha_layout.addLayout(service_layout)

        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel("API Key:"))
        self.key_edit = QLineEdit(self.config.get("captcha_key", ""))
        self.key_edit.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        key_layout.addWidget(self.key_edit)
        captcha_layout.addLayout(key_layout)
        
        captcha_group.setLayout(captcha_layout)
        layout.addWidget(captcha_group)

        # 2. Scheduler Section
        scheduler_group = QGroupBox("📅 Lên lịch chạy tự động (Scheduler)")
        scheduler_layout = QVBoxLayout()

        self.check_enable_scheduler = QCheckBox("Kích hoạt chế độ chạy theo lịch")
        self.check_enable_scheduler.setChecked(self.config.get("scheduler_enabled", False))
        scheduler_layout.addWidget(self.check_enable_scheduler)

        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel("Thời gian bắt đầu mỗi ngày:"))
        self.time_start = QTimeEdit()
        start_time_str = self.config.get("scheduler_time", "08:00")
        self.time_start.setTime(QTime.fromString(start_time_str, "HH:mm"))
        time_layout.addWidget(self.time_start)
        scheduler_layout.addLayout(time_layout)

        days_layout = QHBoxLayout()
        days_layout.addWidget(QLabel("Số ngày chạy liên tục:"))
        self.spin_days = QSpinBox()
        self.spin_days.setRange(1, 365)
        self.spin_days.setValue(self.config.get("scheduler_days", 7))
        days_layout.addWidget(self.spin_days)
        scheduler_layout.addLayout(days_layout)

        auto_close_layout = QHBoxLayout()
        self.check_auto_close = QCheckBox("Tự động đóng trình duyệt sau khi chạy xong kịch bản")
        self.check_auto_close.setChecked(self.config.get("auto_close_enabled", True))
        auto_close_layout.addWidget(self.check_auto_close)
        scheduler_layout.addWidget(self.check_auto_close)

        scheduler_group.setLayout(scheduler_layout)
        layout.addWidget(scheduler_group)

        # Save Button
        self.btn_save = QPushButton(" 💾 Lưu cài đặt & Áp dụng lịch")
        self.btn_save.setObjectName("ActionButton")
        self.btn_save.setFixedWidth(250)
        self.btn_save.clicked.connect(self.save_config)
        layout.addWidget(self.btn_save)

        layout.addStretch()
        self.setLayout(layout)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    self.config = json.load(f)
            except: self.config = {}
        else: self.config = {}

    def save_config(self):
        self.config["captcha_service"] = self.service_combo.currentText()
        self.config["captcha_key"] = self.key_edit.text()
        self.config["scheduler_enabled"] = self.check_enable_scheduler.isChecked()
        self.config["scheduler_time"] = self.time_start.time().toString("HH:mm")
        self.config["scheduler_days"] = self.spin_days.value()
        self.config["auto_close_enabled"] = self.check_auto_close.isChecked()

        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)
            QMessageBox.information(self, "Thành công", "Đã lưu cài đặt và cập nhật lịch trình!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể lưu cài đặt: {e}")