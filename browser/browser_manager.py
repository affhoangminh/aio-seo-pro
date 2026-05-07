from concurrent.futures import ThreadPoolExecutor
from browser.browser_launcher import launch_browser

MAX_BROWSER = 10

executor = ThreadPoolExecutor(MAX_BROWSER)

def open_profiles(profile_list):

    for profile in profile_list:

        executor.submit(launch_browser, profile)

def get_profiles():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    SELECT profiles.id,
           profiles.name,
           proxies.host,
           proxies.port,
           proxies.username,
           proxies.password
    FROM profiles
    LEFT JOIN proxies
    ON profiles.proxy_id = proxies.id
    """)

    rows = cur.fetchall()

    conn.close()

    return rows