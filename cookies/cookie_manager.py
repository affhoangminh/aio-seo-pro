import json
import os

COOKIE_DIR = "cookies"

os.makedirs(COOKIE_DIR, exist_ok=True)

def save_cookies(profile_id, context):

    try:
        cookies = context.cookies()
        
        cookie_file = os.path.join(COOKIE_DIR, f"cookies_{profile_id}.json")
        
        with open(cookie_file, "w") as f:
            json.dump(cookies, f)
            
    except Exception as e:
        if "closed" in str(e).lower():
            pass
        else:
            print(f"Could not save cookies for profile {profile_id}: {e}")

def load_cookies(profile_id, context):

    path = os.path.join(COOKIE_DIR, f"cookies_{profile_id}.json")

    if not os.path.exists(path):
        return

    with open(path, "r") as f:

        cookies = json.load(f)

    context.add_cookies(cookies)