
import json
import random
from bot.page_actions import (
    random_sleep, scroll_page, simulate_reading, 
    simulate_bounce, click_random_internal, 
    goto_url, search_google, find_and_click_domain
)
from bot.mouse_ai import random_mouse_moves

def execute_script(page, script_data):
    """
    Thực thi kịch bản từ JSON. Hỗ trợ cả định dạng List trực tiếp hoặc Dict có khóa 'steps'.
    """
    # 1. Chuẩn hóa dữ liệu đầu vào
    if isinstance(script_data, str):
        try:
            script_data = json.loads(script_data)
        except Exception as e:
            print(f"Lỗi phân tích JSON: {e}")
            return

    # 2. Lấy danh sách các bước (hỗ trợ cả khóa 'steps' hoặc list trực tiếp)
    if isinstance(script_data, dict) and "steps" in script_data:
        steps = script_data["steps"]
    elif isinstance(script_data, list):
        steps = script_data
    else:
        print("Định dạng kịch bản không hợp lệ (phải là List hoặc Dict có khóa 'steps')")
        return

    print(f"🚀 Bắt đầu thực thi kịch bản với {len(steps)} bước...")

    for i, step in enumerate(steps):
        if page.is_closed(): break
        
        # Hỗ trợ cả 'action' và 'type' để linh hoạt
        action = step.get("action") or step.get("type")
        if not action: continue

        print(f"[{i+1}/{len(steps)}] Đang thực hiện: {action}")

        try:
            if action == "goto":
                goto_url(page, step.get("url"))

            elif action == "search_google":
                search_google(page, step.get("keyword"))

            elif action == "click_domain":
                find_and_click_domain(page, step.get("domain"), max_pages=step.get("max_pages", 3))

            elif action == "simulate_reading":
                dur = step.get("duration") or step.get("min", 60)
                simulate_reading(page, min_time=dur, max_time=dur + 30)

            elif action == "scroll":
                scroll_page(page, scroll_steps=step.get("steps", 10))

            elif action == "click_internal":
                # Hỗ trợ tìm theo pattern (ví dụ: 'bao-gia')
                pattern = step.get("pattern")
                if pattern:
                    # Logic click theo pattern có thể được bổ sung trong page_actions
                    # Hiện tại tạm dùng click ngẫu nhiên
                    click_random_internal(page)
                else:
                    for _ in range(step.get("count", 1)):
                        click_random_internal(page)

            elif action == "mouse_move":
                random_mouse_moves(page)

            elif action == "wait":
                sec = step.get("duration") or step.get("seconds", 5)
                random_sleep(sec, sec + 2)

            elif action == "bounce":
                simulate_bounce(page)

        except Exception as e:
            print(f"⚠️ Lỗi thực hiện bước {action}: {e}")

    print("✅ Hoàn thành kịch bản.")
