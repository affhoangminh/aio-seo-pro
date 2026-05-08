import json
import os
import time

from browser.playwright_manager import start_playwright
from browser.browser_pool import register_context

from browser.anti_detect_engine import inject
from browser.network_optimizer import chromium_args

from cookies.cookie_manager import load_cookies, save_cookies
from bot.traffic_bot import run_traffic_bot


PROFILE_DIR = "browser_profiles"
CHROME_PATH = "chromium/chrome.exe"


# ==========================
# PARSE PROXY
# ==========================

def parse_proxy(proxy_string):

    if not proxy_string or proxy_string == "No Proxy":
        return None

    try:

        # user:pass@host:port
        if "@" in proxy_string:

            auth, hostport = proxy_string.split("@")

            username, password = auth.split(":")
            host, port = hostport.split(":")

            return {
                "server": f"http://{host}:{port}",
                "username": username,
                "password": password
            }

        parts = proxy_string.split(":")

        # host:port:user:pass
        if len(parts) == 4:

            host = parts[0]
            port = parts[1]
            username = parts[2]
            password = parts[3]

            return {
                "server": f"http://{host}:{port}",
                "username": username,
                "password": password
            }

        # host:port
        if len(parts) == 2:

            host = parts[0]
            port = parts[1]

            return {
                "server": f"http://{host}:{port}"
            }

    except Exception as e:

        print("Proxy parse error:", e)

    return None


# ==========================
# PARSE FINGERPRINT
# ==========================

def parse_fingerprint(fingerprint_data):

    try:
        fingerprint = json.loads(fingerprint_data)
    except:

        fingerprint = {
            "user_agent": "Mozilla/5.0",
            "resolution": "1280x800"
        }

    resolution = fingerprint.get("resolution", "1280x800")

    width = int(resolution.split("x")[0])
    height = int(resolution.split("x")[1])

    return fingerprint, width, height


# ==========================
# LAUNCH BROWSER
# ==========================

def launch_browser(profile, bot_mode=False):

    profile_id = profile[0]
    proxy_string = profile[2]
    fingerprint_data = profile[3]

    fingerprint, width, height = parse_fingerprint(fingerprint_data)

    profile_path = os.path.join(PROFILE_DIR, f"profile_{profile_id}")
    os.makedirs(profile_path, exist_ok=True)

    proxy_config = parse_proxy(proxy_string)

    print("Launching profile:", profile_id)
    print("Proxy raw:", proxy_string)
    print("Proxy config:", proxy_config)

    try:

        playwright_inst, chromium = start_playwright()

        # Tìm đường dẫn Chrome thực tế trên Windows
        chrome_paths = [
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
            os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe")
        ]
        
        executable_path = None
        for path in chrome_paths:
            if os.path.exists(path):
                executable_path = path
                break

        # Cấu hình khởi chạy để giống người thật 100%
        launch_args = [
            "--disable-blink-features=AutomationControlled", # Quan trọng: Ẩn cờ tự động
            "--no-sandbox",
            "--disable-infobars", # Ẩn dòng "Chrome is being controlled by automated software"
            "--window-position=0,0",
            "--ignore-certificate-errors",
        ] + chromium_args()
        
        context = chromium.launch_persistent_context(
            user_data_dir=profile_path,
            executable_path=executable_path, # Sử dụng Chrome thật nếu tìm thấy
            headless=False,
            proxy=proxy_config,
            args=launch_args,
            ignore_default_args=["--enable-automation"], # Ép buộc xóa bỏ thông báo tự động
            user_agent=fingerprint.get("user_agent"),
            viewport={
                "width": width,
                "height": height
            }

        )

        # register context vào browser pool
        register_context(context)

        # inject anti-detect scripts
        inject(context, fingerprint)

        # block heavy resources for speed
        def block_aggressively(route):
            if route.request.resource_type in ["image", "media", "font"]:
                route.abort()
            else:
                route.continue_()

        # context.route("**/*", block_aggressively) # Uncomment to block images

        # load cookies
        load_cookies(profile_id, context)

        # lấy page đầu tiên
        if context.pages:
            page = context.pages[0]
        else:
            page = context.new_page()

        start = time.time()

        # ==========================
        # BOT MODE OR MANUAL
        # ==========================
        
        end = time.time()
        print("Browser started successfully in:", round(end - start, 2), "seconds")

        if bot_mode:
            print("Bot mode activated. Running traffic bot...")
            
            script_content = None
            if len(profile) > 4 and profile[4]:
                script_path = profile[4]
                if os.path.exists(script_path):
                    try:
                        with open(script_path, 'r', encoding='utf-8') as f:
                            script_content = json.load(f)
                        print(f"Loaded script from: {script_path}")
                    except Exception as e:
                        print(f"Error loading script file: {e}")
            
            try:
                run_traffic_bot(page, script=script_content)
            except Exception as e:
                print("Traffic Bot Error:", e)

        print("Browser started successfully")

        def on_close():
            save_cookies(profile_id, context)
            playwright_inst.stop()

        # khi browser đóng → save cookies
        context.on(
            "close",
            on_close
        )

        # giữ browser chạy
        context.wait_for_event("close")

    except Exception as e:

        print("Browser launch error:", e)