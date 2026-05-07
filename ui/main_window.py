from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QStackedWidget
)

from ui.sidebar import Sidebar
from ui.profiles_page import ProfilesPage
from ui.proxy_page import ProxyPage
from ui.settings_page import SettingsPage


class MainWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("AIO SEO PRO")
        self.resize(1200, 700)

        # =========================
        # MAIN LAYOUT
        # =========================

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # =========================
        # SIDEBAR
        # =========================

        self.sidebar = Sidebar()
        self.sidebar.setFixedWidth(180)

        # =========================
        # PAGES STACK
        # =========================

        self.pages = QStackedWidget(self)

        self.page_profiles = ProfilesPage()
        self.page_proxy = ProxyPage()
        self.page_settings = SettingsPage()

        self.pages.addWidget(self.page_profiles)
        self.pages.addWidget(self.page_proxy)
        self.pages.addWidget(self.page_settings)

        # =========================
        # ADD TO LAYOUT
        # =========================

        layout.addWidget(self.sidebar)
        layout.addWidget(self.pages, 1)

        # =========================
        # MENU EVENTS
        # =========================

        self.sidebar.btn_profiles.clicked.connect(
            lambda: self.pages.setCurrentIndex(0)
        )

        self.sidebar.btn_proxy.clicked.connect(
            lambda: self.pages.setCurrentIndex(1)
        )

        self.sidebar.btn_settings.clicked.connect(
            lambda: self.pages.setCurrentIndex(2)
        )

        # =========================
        # DEFAULT PAGE
        # =========================

        self.pages.setCurrentIndex(0)