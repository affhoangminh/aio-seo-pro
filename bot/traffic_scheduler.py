import random
import time
from browser.browser_worker import add_task
from browser.browser_launcher import launch_browser


class TrafficScheduler:

    def __init__(self, profiles):

        self.profiles = profiles

    def run(self, visits_per_day=1000):

        interval = (24*60*60) / visits_per_day

        print("Traffic interval:", interval)

        while True:

            profile = random.choice(self.profiles)

            add_task(launch_browser, profile)

            sleep_time = random.uniform(
                interval*0.5,
                interval*1.5
            )

            time.sleep(sleep_time)