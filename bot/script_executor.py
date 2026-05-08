
import json
import random
from bot.page_actions import (
    random_sleep, scroll_page, simulate_reading, 
    simulate_bounce, click_random_internal, 
    goto_url, search_google, find_and_click_domain
)
from bot.mouse_ai import random_mouse_moves

def execute_script(page, script_json):
    """
    Thực thi một bộ kịch bản dựa trên JSON.
    Cấu trúc: [ {"type": "goto", "url": "..."}, {"type": "search", "keyword": "..."}, ... ]
    """

    try:
        steps = json.loads(script_json) if isinstance(script_json, str) else script_json
    except Exception as e:
        print(f"Lỗi phân tích kịch bản: {e}")
        return

    print(f"Bắt đầu thực thi kịch bản với {len(steps)} bước...")

    for i, step in enumerate(steps):
        step_type = step.get("type")
        print(f"[{i+1}/{len(steps)}] Đang thực hiện: {step_type}")

        try:
            if step_type == "goto":
                goto_url(page, step.get("url"))

            elif step_type == "search_google":
                search_google(page, step.get("keyword"))

            elif step_type == "click_domain":
                find_and_click_domain(page, step.get("domain"), max_pages=step.get("max_pages", 3))

            elif step_type == "simulate_reading":
                simulate_reading(
                    page, 
                    min_time=step.get("min", 60), 
                    max_time=step.get("max", 180)
                )

            elif step_type == "scroll":
                scroll_page(page)

            elif step_type == "click_internal":
                for _ in range(step.get("count", 1)):
                    click_random_internal(page)

            elif step_type == "mouse_move":
                random_mouse_moves(page)

            elif step_type == "wait":
                random_sleep(step.get("seconds", 5), step.get("seconds", 5) + 2)

            elif step_type == "bounce":
                simulate_bounce(page)

        except Exception as e:
            print(f"Lỗi thực hiện bước {step_type}: {e}")

    print("Hoàn thành kịch bản.")
