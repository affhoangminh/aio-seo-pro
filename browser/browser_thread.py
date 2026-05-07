import threading
from browser.browser_launcher import launch_browser

threads = []

def open_browser(profile):

    t = threading.Thread(
        target=launch_browser,
        args=(profile,),
        daemon=True
    )

    threads.append(t)

    t.start()