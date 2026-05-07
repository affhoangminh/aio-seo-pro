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
# SIMULATE READING (DWELL TIME)
# ======================

def simulate_reading(page, min_time=180, max_time=300):
    total_time = random.uniform(min_time, max_time)
    start_time = time.time()
    
    print(f"Bắt đầu giả lập đọc (Dwell Time) trong {int(total_time)} giây...")
    
    while time.time() - start_time < total_time:
        # Cuộn trang lên/xuống (thiên về cuộn xuống)
        direction = random.choice([1, -1, 1, 1])
        step = random.randint(100, 500) * direction
        page.mouse.wheel(0, step)
        
        # Giả lập bôi đen văn bản khi đọc (30% cơ hội)
        if random.random() < 0.3:
            try:
                viewport = page.viewport_size
                if viewport:
                    start_x = random.randint(100, viewport['width'] - 100)
                    start_y = random.randint(100, viewport['height'] - 100)
                    end_x = start_x + random.randint(50, 300)
                    end_y = start_y + random.randint(10, 50)
                    
                    page.mouse.move(start_x, start_y)
                    page.mouse.down()
                    page.mouse.move(end_x, end_y, steps=random.randint(5, 15))
                    page.mouse.up()
            except:
                pass
                
        # Thỉnh thoảng click ra ngoài để bỏ bôi đen
        if random.random() < 0.1:
            try:
                page.mouse.click(10, 10)
            except:
                pass
            
        random_sleep(2, 6)

# ======================
# SIMULATE BOUNCE RATE
# ======================

def simulate_bounce(page):
    bounce_time = random.uniform(5, 15)
    print(f"Giả lập Bounce Rate: Thoát trang sau {int(bounce_time)} giây...")
    
    # Cuộn 1-2 lần rồi dừng
    for _ in range(random.randint(1, 2)):
        page.mouse.wheel(0, random.randint(200, 600))
        random_sleep(1, 3)
        
    time.sleep(bounce_time)

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