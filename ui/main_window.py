
import json
import os
import threading
import time
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QStackedWidget,
    QMessageBox
)
from PySide6.QtCore import QTimer, QTime, QDate

from ui.sidebar import Sidebar
from ui.profiles_page import ProfilesPage
from ui.proxy_page import ProxyPage
from ui.settings_page import SettingsPage
from ui.script_manager_page import ScriptManagerPage
from ui.schedule_page import SchedulePage
from ui.styles import MAIN_STYLES

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AIO SEO PRO - Hệ thống tăng Traffic & Seeding")
        self.resize(1200, 800)
        self.setStyleSheet(MAIN_STYLES)

        # UI Components
        self.setup_ui()
        
        # Scheduler Timer
        self.scheduler_timer = QTimer(self)
        self.scheduler_timer.timeout.connect(self.check_scheduler)
        self.scheduler_timer.start(60000) # Kiểm tra mỗi phút

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()

        # Pages Stack
        self.pages = QStackedWidget(self)
        self.pages.setContentsMargins(20, 20, 20, 20)

        self.page_profiles = ProfilesPage()
        self.page_proxy = ProxyPage()
        self.page_scripts = ScriptManagerPage()
        self.page_schedule = SchedulePage()
        self.page_settings = SettingsPage()

        self.pages.addWidget(self.page_profiles)
        self.pages.addWidget(self.page_proxy)
        self.pages.addWidget(self.page_scripts)
        self.pages.addWidget(self.page_schedule)
        self.pages.addWidget(self.page_settings)

        layout.addWidget(self.sidebar)
        layout.addWidget(self.pages, 1)

        # Signals
        self.sidebar.btn_profiles.clicked.connect(lambda: self.switch_page(self.page_profiles, self.sidebar.btn_profiles))
        self.sidebar.btn_proxy.clicked.connect(lambda: self.switch_page(self.page_proxy, self.sidebar.btn_proxy))
        self.sidebar.btn_scripts.clicked.connect(lambda: self.switch_page(self.page_scripts, self.sidebar.btn_scripts))
        self.sidebar.btn_schedule.clicked.connect(lambda: self.switch_page(self.page_schedule, self.sidebar.btn_schedule))
        self.sidebar.btn_settings.clicked.connect(lambda: self.switch_page(self.page_settings, self.sidebar.btn_settings))
        
        # Connect Manual Run Signal
        self.page_schedule.runRequested.connect(lambda data: threading.Thread(target=self.execute_campaign, args=(data,), daemon=True).start())

    def switch_page(self, page, button):
        self.pages.setCurrentWidget(page)
        self.sidebar.set_active(button)

    def check_scheduler(self):
        # New complex scheduler logic
        from profiles.profile_manager import get_schedules
        from datetime import datetime, timedelta
        
        schedules = get_schedules()
        now_dt = datetime.now()
        now_time = now_dt.strftime("%HH:%mm") # Simplified for matching
        
        # Actually checking HH:mm is better
        current_time_str = QTime.currentTime().toString("HH:mm")
        current_date_str = QDate.currentDate().toString("yyyy-MM-dd")
        
        for sch in schedules:
            # sch_id, name, profile_id, start_date, start_time, duration_days, is_active, scripts_json, run_mode
            if sch[6] == 0: continue # OFF
            
            start_date = datetime.strptime(sch[3], "%Y-%m-%d")
            end_date = start_date + timedelta(days=sch[5])
            
            if start_date.date() <= now_dt.date() <= end_date.date():
                if current_time_str == sch[4]:
                    print(f"⏰ Kích hoạt chiến dịch: {sch[1]}")
                    threading.Thread(target=self.execute_campaign, args=(sch,), daemon=True).start()

    def execute_campaign(self, campaign_data):
        from browser.browser_launcher import launch_browser
        from profiles.profile_manager import get_profile, get_profiles
        import random
        
        profile_id = campaign_data[2]
        scripts = json.loads(campaign_data[7])
        run_mode = campaign_data[8]
        
        # Profile selection logic
        target_profile = None
        if profile_id == 0: # Random
            all_p = get_profiles()
            if all_p: target_profile = random.choice(all_p)
        elif profile_id == -1: # Fallback (Logic needed)
            all_p = get_profiles()
            # Try first, if fail, try next...
            target_profile = all_p[0] if all_p else None
        else:
            target_profile = get_profile(profile_id)
            
        if not target_profile:
            print("❌ Không tìm thấy Profile để thực hiện chiến dịch.")
            return

        # Execute sequence of scripts
        for s in scripts:
            print(f"🚀 Chiến dịch {campaign_data[1]}: Chạy script {os.path.basename(s['path'])}")
            
            # Pack profile data with the specific script path for this step
            # Note: We need to adapt launch_browser to accept a dynamic script or we pass it via bot_mode
            # For now, let's assume we modify launch_browser to handle this
            
            # We override the profile[4] (script_path) with s['path']
            mod_profile = list(target_profile)
            if len(mod_profile) <= 4: mod_profile.append(s['path'])
            else: mod_profile[4] = s['path']
            
            # Run browser in a new thread for each script? 
            # Or sequentially? Sequential is better for one profile.
            
            # Since launch_browser is blocking (due to wait_for_event), 
            # we need to be careful.
            
            launch_browser(mod_profile, bot_mode=True)
            
            # Delay between scripts (minutes)
            delay_min = s['delay']
            if delay_min > 0:
                print(f"⏳ Nghỉ {delay_min} phút trước script tiếp theo...")
                time.sleep(delay_min * 60)