from multiprocessing import Process
from browser.browser_launcher import launch_browser

processes = []


def open_browser(profile):

    p = Process(
        target=launch_browser,
        args=(profile,)
    )

    processes.append(p)

    p.start()