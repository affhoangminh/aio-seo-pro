import random

from bot.page_actions import scroll_page
from bot.page_actions import click_random_internal
from bot.page_actions import random_sleep

from bot.mouse_ai import random_mouse_moves


def run_traffic_bot(page):

    random_mouse_moves(page)

    scroll_page(page)

    random_sleep(3,6)

    for _ in range(random.randint(1,4)):

        click_random_internal(page)

        scroll_page(page)

        random_sleep(4,8)