
import json
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QTableWidget, QTableWidgetItem, QPushButton, 
    QHeaderView, QMessageBox, QAbstractItemView
)
from PySide6.QtCore import Qt, Signal
from profiles.profile_manager import get_schedules, delete_schedule, toggle_schedule
from ui.schedule_dialog import ScheduleDialog

class SchedulePage(QWidget):
    runRequested = Signal(tuple)

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Header Buttons (Toolbar)
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton(" ➕ Thêm mới")
        self.btn_add.setObjectName("ActionButton")
        self.btn_add.clicked.connect(self.add_schedule)
        
        self.btn_edit = QPushButton(" ✏️ Sửa")
        self.btn_edit.setObjectName("SecondaryButton")
        self.btn_edit.clicked.connect(self.edit_selected)

        self.btn_delete = QPushButton(" 🗑️ Xóa")
        self.btn_delete.setObjectName("DangerButton")
        self.btn_delete.clicked.connect(self.delete_selected)

        self.btn_refresh = QPushButton(" 🔄 Làm mới")
        self.btn_refresh.clicked.connect(self.load_data)

        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_refresh)
        layout.addLayout(btn_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Tên Lịch trình", "Profile", "Thời gian bắt đầu", "Số ngày", "Trạng thái", "Thao tác"
        ])
        
        # Style header
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(6, QHeaderView.Fixed)
        self.table.setColumnWidth(6, 200)
        self.table.setColumnHidden(0, True)
        
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(50) # Fix chiều cao dòng
        
        layout.addWidget(self.table)
        self.setLayout(layout)

    def load_data(self):
        self.table.setRowCount(0)
        schedules = get_schedules()
        
        for sch in schedules:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Lưu dữ liệu thô vào row để dễ truy xuất
            self.table.setItem(row, 0, QTableWidgetItem(str(sch[0])))
            self.table.setItem(row, 1, QTableWidgetItem(sch[1]))
            
            from profiles.profile_manager import get_profile
            p_id = sch[2]
            p_name = "Random" if p_id == 0 else "Fallback" if p_id == -1 else "Unknown"
            if p_id > 0:
                p_data = get_profile(p_id)
                if p_data: p_name = p_data[1]
            self.table.setItem(row, 2, QTableWidgetItem(p_name))
            self.table.setItem(row, 3, QTableWidgetItem(f"{sch[3]} {sch[4]}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{sch[5]} ngày"))
            
            status_text = "🟢 ON" if sch[6] == 1 else "🔴 OFF"
            status_item = QTableWidgetItem(status_text)
            status_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 5, status_item)
            
            # Actions Widget
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 2, 5, 2)
            
            btn_play = QPushButton("▶️ Chạy")
            btn_play.clicked.connect(lambda _, s=sch: self.run_now(s))
            
            btn_toggle = QPushButton("ON/OFF")
            btn_toggle.clicked.connect(lambda _, s=sch: self.toggle_active(s))
            
            actions_layout.addWidget(btn_play)
            actions_layout.addWidget(btn_toggle)
            self.table.setCellWidget(row, 6, actions_widget)

    def add_schedule(self):
        if ScheduleDialog().exec(): self.load_data()

    def edit_selected(self):
        row = self.table.currentRow()
        if row >= 0:
            sch_id = int(self.table.item(row, 0).text())
            # Tìm dữ liệu đầy đủ từ DB
            schedules = get_schedules()
            sch_data = next((s for s in schedules if s[0] == sch_id), None)
            if sch_data and ScheduleDialog(sch_data).exec():
                self.load_data()

    def delete_selected(self):
        row = self.table.currentRow()
        if row >= 0:
            sch_id = int(self.table.item(row, 0).text())
            if QMessageBox.question(self, "Xác nhận", "Xóa lịch trình này?") == QMessageBox.Yes:
                delete_schedule(sch_id)
                self.load_data()

    def toggle_active(self, schedule_data):
        new_status = 1 if schedule_data[6] == 0 else 0
        toggle_schedule(schedule_data[0], new_status)
        self.load_data()

    def run_now(self, schedule_data):
        self.runRequested.emit(schedule_data)
