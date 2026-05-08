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

# ======================

# GOTO URL
# ======================

def goto_url(page, url):
    print(f"Truy cập URL: {url}")
    page.goto(url, wait_until="domcontentloaded")
    check_captcha(page)
    random_sleep(2, 4)


# ======================
# HUMAN-LIKE TYPING
# ======================

def human_type(page, selector, text):
    element = page.query_selector(selector)
    if element:
        element.click()
        for char in text:
            page.keyboard.type(char, delay=random.randint(50, 250))
            if random.random() < 0.1: # 10% cơ hội dừng lại một chút như đang nghĩ
                random_sleep(0.5, 1.5)

# ======================
# CHECK CAPTCHA
# ======================

def check_captcha(page):
    captcha_indicators = [
        "https://www.google.com/sorry/index",
        "detected unusual traffic",
        "recaptcha"
    ]
    
    try:
        current_url = page.url
        # Kiểm tra qua URL trước cho nhanh
        is_captcha = any(ind in current_url for ind in captcha_indicators)
        
        if not is_captcha:
            # Nếu URL không rõ, kiểm tra nội dung trang
            page_content = page.content().lower()
            is_captcha = any(ind in page_content for ind in captcha_indicators)
            
        if is_captcha:
            print("⚠️ CẢNH BÁO: Phát hiện Google CAPTCHA! Vui lòng giải tay trên trình duyệt để tiếp tục.")
            while any(ind in page.url for ind in captcha_indicators):
                time.sleep(5)
            print("✅ CAPTCHA đã được giải. Tiếp tục kịch bản...")
            return True
    except:
        pass
    return False


# ======================
# SEARCH GOOGLE
# ======================

def search_google(page, keyword):
    print(f"Tìm kiếm Google với từ khóa: {keyword}")
    page.goto("https://www.google.com", wait_until="domcontentloaded")
    random_sleep(2, 3)
    
    # Kiểm tra captcha ngay khi vào Google
    check_captcha(page)
    
    # Tìm ô search (xử lý cả id và name)
    search_selector = "textarea[name='q'], input[name='q']"
    search_box = page.query_selector(search_selector)
    
    if search_box:
        # Sử dụng human_type thay vì fill
        human_type(page, search_selector, keyword)
        random_sleep(1, 2)
        page.keyboard.press("Enter")
        page.wait_for_load_state("domcontentloaded")
        
        # Kiểm tra captcha sau khi search
        check_captcha(page)
        random_sleep(3, 5)


# ======================
# FIND AND CLICK DOMAIN IN GOOGLE
# ======================

def find_and_click_domain(page, domain, max_pages=10):
    print(f"Tìm kiếm domain '{domain}' trong kết quả Google (Tối đa {max_pages} trang)...")
    
    for p in range(max_pages):
        print(f"--- Đang quét trang {p+1} ---")
        random_sleep(3, 5) # Đợi trang tải xong hẳn
        
        # Lấy tất cả các link <a>
        links = page.query_selector_all("a")
        
        for link in links:
            try:
                href = link.get_attribute("href")
                if href and domain in href:
                    if "googleadservices" in href: continue
                    
                    print(f"🔥 Đã tìm thấy domain tại trang {p+1}. Đang click...")
                    link.scroll_into_view_if_needed()
                    random_sleep(1, 2)
                    link.click()
                    page.wait_for_load_state("domcontentloaded")
                    return True
            except:
                continue
        
        # Tìm nút chuyển trang (Hỗ trợ cả Tiếng Anh và Tiếng Việt)
        next_selectors = [
            "#pnnext", 
            "a[aria-label='Next page']", 
            "a:has-text('Next')", 
            "a:has-text('Tiếp')",
            "a:has-text('Trang sau')"
        ]
        
        next_btn = None
        for sel in next_selectors:
            next_btn = page.query_selector(sel)
            if next_btn: break
            
        if next_btn:
            print(f"Chuyển sang trang {p+2}...")
            next_btn.scroll_into_view_if_needed()
            random_sleep(1, 2)
            next_btn.click()
            page.wait_for_load_state("domcontentloaded")
            check_captcha(page)
        else:
            # Nếu không thấy nút Next, thực hiện cuộn để kích hoạt Continuous Scroll (Google mới)
            print("Không thấy nút chuyển trang, thử cuộn xuống cuối trang để tải thêm...")
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            random_sleep(4, 6)
            check_captcha(page)



            
    print(f"Không tìm thấy domain '{domain}' sau {max_pages} trang.")
    return False