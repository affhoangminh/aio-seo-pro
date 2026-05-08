import sys
import threading

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow

from qt_material import apply_stylesheet

from profiles.profile_manager import init_db

from browser.browser_pool import close_all
from browser.playwright_manager import stop_playwright
from browser.browser_worker import start_workers


# ==========================
# CLEANUP FUNCTION
# ==========================

def cleanup():

    print("Closing browsers...")

    try:
        close_all()
    except Exception as e:
        print("close_all error:", e)

    try:
        stop_playwright()
    except Exception as e:
        print("stop_playwright error:", e)

    print("All browsers closed")


# ==========================
# CLEANUP THREAD
# ==========================

def cleanup_async():

    thread = threading.Thread(
        target=cleanup,
        daemon=True
    )

    thread.start()


# ==========================
# MAIN
# ==========================

def main():

    print("Starting AIO SEO PRO...")

    # init database
    init_db()

    # start browser workers
    start_workers()

    # create Qt app
    app = QApplication(sys.argv)

    # apply UI theme
    from ui.styles import MAIN_STYLES
    apply_stylesheet(app, theme="light_blue.xml")
    app.setStyleSheet(app.styleSheet() + MAIN_STYLES)


    # cleanup when closing
    app.aboutToQuit.connect(cleanup_async)


    # open main window
    window = MainWindow()
    window.show()

    # start UI loop
    sys.exit(app.exec())


# ==========================
# PROGRAM ENTRY
# ==========================

if __name__ == "__main__":
    main()