import random
import time


def human_mouse_move(page, x, y):

    current_x = random.randint(0, 400)
    current_y = random.randint(0, 400)

    steps = random.randint(20, 40)

    dx = (x - current_x) / steps
    dy = (y - current_y) / steps

    for i in range(steps):

        current_x += dx
        current_y += dy

        page.mouse.move(current_x, current_y)

        time.sleep(random.uniform(0.01, 0.03))


def random_mouse_moves(page):

    for _ in range(random.randint(3,8)):

        x = random.randint(0,1200)
        y = random.randint(0,800)

        human_mouse_move(page,x,y)

        time.sleep(random.uniform(0.3,1.2))