import random

from bot.page_actions import scroll_page, simulate_reading, simulate_bounce
from bot.page_actions import click_random_internal
from bot.page_actions import random_sleep

from bot.mouse_ai import random_mouse_moves


from bot.script_executor import execute_script

def run_traffic_bot(page, script=None):
    
    if script:
        execute_script(page, script)
        return

    random_mouse_moves(page)


    # Giả lập 20% tỷ lệ Bounce Rate (thoát trang ngay)
    if random.random() < 0.20:
        simulate_bounce(page)
        return

    # 80% còn lại sẽ là Dwell Time (Đọc kỹ trang đích)
    # Rút ngắn thời gian min/max để test nhanh (Ví dụ: 60 - 180s)
    simulate_reading(page, min_time=60, max_time=180)

    # Click nội bộ để tạo phiên sâu hơn
    for _ in range(random.randint(1,4)):

        click_random_internal(page)

        # Trang nội bộ đọc nhanh hơn một chút
        simulate_reading(page, min_time=30, max_time=90)