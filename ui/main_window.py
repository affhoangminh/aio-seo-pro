from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QStackedWidget
)

from ui.sidebar import Sidebar
from ui.profiles_page import ProfilesPage
from ui.proxy_page import ProxyPage
from ui.settings_page import SettingsPage
from ui.script_manager_page import ScriptManagerPage



from ui.styles import MAIN_STYLES


class MainWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("AIO SEO PRO - Hệ thống tăng Traffic & Seeding")
        self.resize(1200, 800)
        self.setStyleSheet(MAIN_STYLES)

        # =========================
        # MAIN LAYOUT
        # =========================

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # =========================
        # SIDEBAR
        # =========================

        self.sidebar = Sidebar()

        # =========================
        # PAGES STACK
        # =========================

        self.pages = QStackedWidget(self)
        self.pages.setContentsMargins(20, 20, 20, 20)

        self.page_profiles = ProfilesPage()
        self.page_proxy = ProxyPage()
        self.page_scripts = ScriptManagerPage()
        self.page_settings = SettingsPage()

        self.pages.addWidget(self.page_profiles)
        self.pages.addWidget(self.page_proxy)
        self.pages.addWidget(self.page_scripts)
        self.pages.addWidget(self.page_settings)


        # =========================
        # ADD TO LAYOUT
        # =========================

        layout.addWidget(self.sidebar)
        layout.addWidget(self.pages, 1)

        # =========================
        # MENU EVENTS
        # =========================

        self.sidebar.btn_profiles.clicked.connect(self.switch_to_profiles)
        self.sidebar.btn_proxy.clicked.connect(self.switch_to_proxy)
        self.sidebar.btn_scripts.clicked.connect(self.switch_to_scripts)
        self.sidebar.btn_settings.clicked.connect(self.switch_to_settings)


        # =========================
        # DEFAULT PAGE
        # =========================

        self.pages.setCurrentIndex(0)

    def switch_to_profiles(self):
        self.pages.setCurrentIndex(0)
        self.sidebar.set_active(self.sidebar.btn_profiles)

    def switch_to_proxy(self):
        self.pages.setCurrentIndex(1)
        self.sidebar.set_active(self.sidebar.btn_proxy)

    def switch_to_scripts(self):
        self.pages.setCurrentIndex(2)
        self.sidebar.set_active(self.sidebar.btn_scripts)

    def switch_to_settings(self):
        self.pages.setCurrentIndex(3)
        self.sidebar.set_active(self.sidebar.btn_settings)
