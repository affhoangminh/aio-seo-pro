
# ui/styles.py

MAIN_STYLES = """
QMainWindow, QWidget {
    background-color: #f8fafc;
    color: #0f172a;
    font-family: "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

/* SIDEBAR STYLES */
#Sidebar {
    background-color: #ffffff;
    border-right: 1px solid #e2e8f0;
    min-width: 200px;
}

#Sidebar QPushButton {
    background-color: transparent;
    border: none;
    color: #64748b;
    text-align: left;
    padding: 12px 20px;
    font-size: 14px;
    font-weight: 500;
    border-radius: 8px;
    margin: 4px 10px;
}

#Sidebar QPushButton:hover {
    background-color: #f1f5f9;
    color: #0f172a;
}

#Sidebar QPushButton[active="true"] {
    background-color: #3b82f6;
    color: #ffffff;
}

#SidebarLabel {
    color: #3b82f6;
    font-size: 18px;
    font-weight: bold;
    padding: 20px;
    margin-bottom: 10px;
}

/* TABLE STYLES */
QTableWidget {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    gridline-color: #f1f5f9;
    outline: none;
    color: #1e293b;
}

QTableWidget::item {
    padding: 10px;
    border-bottom: 1px solid #f1f5f9;
}

QTableWidget::item:selected {
    background-color: #eff6ff;
    color: #3b82f6;
}

QHeaderView::section {
    background-color: #f8fafc;
    color: #64748b;
    padding: 12px;
    border: none;
    border-bottom: 2px solid #3b82f6;
    font-weight: bold;
    font-size: 13px;
}

/* BUTTON STYLES */
QPushButton#ActionButton {
    background-color: #3b82f6;
    color: white;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 600;
    font-size: 13px;
}

QPushButton#ActionButton:hover {
    background-color: #2563eb;
}

QPushButton#SecondaryButton {
    background-color: #e2e8f0;
    color: #475569;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 600;
    font-size: 13px;
}

QPushButton#SecondaryButton:hover {
    background-color: #cbd5e1;
}

QPushButton#DangerButton {
    background-color: #ef4444;
    color: white;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 600;
}

QPushButton#DangerButton:hover {
    background-color: #dc2626;
}

/* LIST WIDGET STYLES */
QListWidget {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    outline: none;
    padding: 5px;
}

QListWidget::item {
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    margin-bottom: 5px;
    padding: 12px;
    color: #1e293b;
}

QListWidget::item:selected {
    background-color: #eff6ff;
    border: 1px solid #3b82f6;
    color: #3b82f6;
}

/* SCROLLBAR STYLES */

QScrollBar:vertical {
    border: none;
    background: #f8fafc;
    width: 10px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #cbd5e1;
    min-height: 20px;
    border-radius: 5px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""

