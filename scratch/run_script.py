import sys
import os
import io

# Reconfigure stdout and stderr to UTF-8 to prevent charmap codec errors on Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from profiles.profile_manager import get_profiles, init_db
from browser.browser_launcher import launch_browser

def main():
    init_db()
    profiles = get_profiles()
    
    # Sử dụng Profile F02 hoặc profile đầu tiên tìm thấy
    p_data = None
    if profiles:
        for p in profiles:
            if p[1] == "F02":
                p_data = p
                break
        if not p_data:
            p_data = profiles[0]
            
    if p_data:
        # p: (id, name, proxy_host, proxy_port, proxy_user, proxy_pass, description)
        proxy = f"{p_data[2]}:{p_data[3]}:{p_data[4]}:{p_data[5]}" if p_data[2] else None
        profile = (p_data[0], p_data[1], proxy, '{"resolution":"1920x1080"}', "scripts/bhminh_mo_claude_script.json")
    else:
        profile = (1, "Test Profile", None, '{"resolution":"1920x1080"}', "scripts/bhminh_mo_claude_script.json")
        
    print(f"Running script bhminh_mo_claude_script.json on profile: {profile[1]} (ID: {profile[0]})")
    launch_browser(profile, bot_mode=True)

if __name__ == "__main__":
    main()
