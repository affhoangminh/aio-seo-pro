
import json
import os
import time
import requests
from anticaptchaofficial.recaptchav2proxyless import *

CONFIG_FILE = "database/config.json"

def get_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {}

def solve_recaptcha_v2(page, website_url):
    config = get_config()
    api_key = config.get("captcha_key")
    service = config.get("captcha_service", "Anti-Captcha")
    
    if not api_key:
        print("❌ Chưa cấu hình API Key trong phần Cài đặt!")
        return False

    # Tìm sitekey trên trang
    site_key = None
    try:
        site_key_element = page.query_selector(".g-recaptcha")
        if site_key_element:
            site_key = site_key_element.get_attribute("data-sitekey")
        
        if not site_key:
            content = page.content()
            import re
            match = re.search(r'data-sitekey=["\'](.*?)["\']', content)
            if match:
                site_key = match.group(1)
    except:
        pass
            
    if not site_key:
        print("❌ Không tìm thấy SiteKey trên trang!")
        return False

    print(f"🚀 Đang gửi yêu cầu giải CAPTCHA tới {service}...")

    if service == "Anti-Captcha":
        solver = recaptchaV2Proxyless()
        solver.set_verbose(1)
        solver.set_key(api_key)
        solver.set_website_url(website_url)
        solver.set_website_key(site_key)
        g_response = solver.solve_and_return_solution()
        
    elif service == "2Captcha":
        # Gọi qua requests cho 2Captcha
        try:
            resp = requests.post(f"http://2captcha.com/in.php?key={api_key}&method=userrecaptcha&googlekey={site_key}&pageurl={website_url}&json=1")
            request_id = resp.json().get("request")
            if not request_id: return False
            
            for _ in range(20):
                time.sleep(5)
                res = requests.get(f"http://2captcha.com/res.php?key={api_key}&action=get&id={request_id}&json=1")
                if res.json().get("status") == 1:
                    g_response = res.json().get("request")
                    break
            else: return False
        except: return False
    else:
        print(f"❌ Dịch vụ {service} chưa được hỗ trợ đầy đủ.")
        return False

    if g_response and g_response != 0:
        print("✅ Đã nhận được lời giải. Đang thực thi...")
        try:
            page.evaluate(f'document.getElementById("g-recaptcha-response").innerHTML="{g_response}";')
            page.evaluate('document.getElementById("captcha-form").submit();')
            time.sleep(3)
            return True
        except:
            return False
    return False
