import random
import time

from bot.page_actions import random_sleep


def search_and_click(page, keyword, target_domain):

    print("Searching:", keyword)

    page.goto("https://www.google.com")

    random_sleep()

    page.fill("textarea[name=q]", keyword)

    page.keyboard.press("Enter")

    page.wait_for_load_state("domcontentloaded")

    random_sleep(3, 5)

    # scroll google
    page.mouse.wheel(0, 800)

    random_sleep()

    links = page.query_selector_all("a")

    for link in links:

        href = link.get_attribute("href")

        if href and target_domain in href:

            print("Click:", href)

            try:
                link.click()
                return True
            except:
                pass

    print("Target not found")

    return False