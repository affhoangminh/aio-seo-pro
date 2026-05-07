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

def launch_browser(profile):

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

        context = chromium.launch_persistent_context(

            executable_path=CHROME_PATH,

            user_data_dir=profile_path,

            headless=False,

            proxy=proxy_config,

            args=chromium_args(),

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
        # MULTI-TAB ROTATION
        # ==========================
        
        print("Opening multiple tabs...")
        pages = []
        
        # Mở 3 tab với các trang khác nhau
        targets = [
            ("https://google.com", "Google"),
            ("https://bing.com", "Bing"),
            ("https://wikipedia.org", "Wikipedia")
        ]

        for url, name in targets:
            try:
                new_page = context.new_page()
                print(f"Opening tab: {name}")
                # Đổi sang domcontentloaded để không bị xoay vòng mãi mãi
                new_page.goto(url, wait_until="domcontentloaded", timeout=30000)
                pages.append(new_page)
                time.sleep(2)
            except Exception as e:
                print(f"Failed to open {name}: {e}")

        # Xoay vòng giữa các tab
        if pages:
            for i in range(2): # Xoay vòng 2 vòng
                for idx, p in enumerate(pages):
                    print(f"Switching to tab {idx+1}")
                    p.bring_to_front()
                    time.sleep(3)
                    # Thực hiện hành động cuộn trang nhẹ
                    p.mouse.wheel(0, 300)
        
        print("Tab rotation finished.")
        end = time.time()

        print("Page loaded in:", round(end - start, 2), "seconds")
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