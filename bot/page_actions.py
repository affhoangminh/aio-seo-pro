import random
import time


def random_sleep(a=1, b=3):
    time.sleep(random.uniform(a, b))


# ======================
# SCROLL PAGE
# ======================

def scroll_page(page):

    height = page.evaluate("document.body.scrollHeight")

    current = 0

    while current < height:

        step = random.randint(300, 800)

        page.mouse.wheel(0, step)

        current += step

        random_sleep(1, 2)


# ======================
# CLICK RANDOM INTERNAL LINK
# ======================

def click_random_internal(page):

    links = page.query_selector_all("a")

    valid_links = []

    for link in links:

        href = link.get_attribute("href")

        if href and href.startswith("/"):

            valid_links.append(link)

    if not valid_links:
        return

    link = random.choice(valid_links)

    try:

        link.click()

        random_sleep(3, 6)

    except:
        pass