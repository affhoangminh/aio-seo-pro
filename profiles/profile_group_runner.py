from browser.browser_worker import add_task
from browser.browser_launcher import launch_browser


def run_profiles(profiles):

    for p in profiles:

        add_task(launch_browser, p)