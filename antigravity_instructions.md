# AIO SEO PRO - Nguyên tắc vận hành & Hướng dẫn kỹ thuật

Tài liệu này ghi lại các thay đổi quan trọng, nguyên lý thiết kế và cơ chế hoạt động của hệ thống AIO SEO PRO (phiên bản tối ưu hóa).

## 1. Kiến trúc hệ thống (System Architecture)

### Đa luồng độc lập (Isolated Multi-threading)
- **Nguyên lý**: Mỗi Profile khi khởi chạy sẽ được cấp một luồng (Thread) riêng biệt.
- **Playwright Instance**: Mỗi luồng sở hữu một instance Playwright (`sync_playwright`) riêng. Điều này giúp tránh hiện tượng nghẽn cổ chai (bottleneck) và tăng tính ổn định khi chạy nhiều profile cùng lúc.
- **Resource Cleanup**: Khi trình duyệt đóng, hệ thống tự động gọi `.stop()` cho instance Playwright tương ứng để giải phóng RAM hoàn toàn.

## 2. Cơ chế Anti-detect (Chống phát hiện)

Hệ thống sử dụng tầng Inject JavaScript (`anti_detect_engine.py`) để làm giả các thông số trình duyệt:

### Lớp bảo vệ WebRTC
- **Vô hiệu hóa WebRTC**: Chặn các hàm `RTCPeerConnection` để ngăn Google/Facebook phát hiện địa chỉ IP thật của máy (IP Leak) đằng sau Proxy.

### Đồng bộ hóa Fingerprint
- **Screen Consistency**: Ép các thông số `screen.width`, `window.innerWidth` phải khớp chính xác với độ phân giải giả lập, tránh bị phát hiện do sự lệch lạc thông số.

### 2.1. Trình duyệt "Thật 100%" (Stealth Browser)
Để vượt qua lớp bảo mật "Browser not secure" của Google:
- **Executable Path**: Hệ thống tự động tìm và sử dụng tệp `chrome.exe` chính chủ được cài đặt trên máy thay vì Chromium đi kèm.
- **Hide Automation Flags**: Loại bỏ cờ `--enable-automation` và sử dụng `--disable-blink-features=AutomationControlled` để xóa bỏ thuộc tính `navigator.webdriver`.
- **User Data Persistence**: Giữ nguyên toàn bộ lịch sử, cache và trạng thái đăng nhập như một trình duyệt thông thường.


## 3. Tối ưu hóa hiệu suất (Performance Optimization)

### Chiến lược tải trang (Loading Strategy)
- **Wait Until**: Sử dụng `wait_until="domcontentloaded"` thay vì `load`. Trình duyệt sẽ bắt đầu xử lý Bot ngay khi khung trang web hiện ra, không đợi tải các tài nguyên rác.
- **HTTP/2**: Luôn bật HTTP/2 để tận dụng khả năng tải dữ liệu song song, giúp tốc độ tải trang nhanh gấp 2-3 lần.
- **Resource Blocking**: Hỗ trợ cơ chế chặn Image/Media/Font (tùy chọn) để tiết kiệm băng thông Proxy.

## 4. Cơ chế Bot & Hành vi tự nhiên

### Chế độ Bot (Bot Mode)
- **Tích hợp UI**: Hệ thống phân tách rõ ràng giữa chế độ duyệt web thủ công (Nút "Mở") và chế độ tự động hóa (Nút "Chạy Traffic Bot").
- **Dwell Time (Đọc hiểu)**: Hàm `simulate_reading()` giữ bot ở lại trang đích một cách ngẫu nhiên (ví dụ 1-3 phút). Trong lúc đó, bot liên tục cuộn trang và có xác suất (30%) bôi đen (highlight) văn bản như đang đọc để vượt qua các bộ lọc Heatmap/Dwell Time khắt khe nhất.
- **Bounce Rate (Tỷ lệ thoát)**: Hàm `simulate_bounce()` chiếm 20% xác suất trong phiên, giả lập người dùng chỉ vào trang vài giây, cuộn 1-2 lần rồi thoát ngay, giúp chỉ số Google Analytics trông tự nhiên.

### Điều khiển chuột (Mouse AI)
- Di chuyển chuột theo quỹ đạo bước (steps) với tốc độ biến thiên, không di chuyển tức thời theo đường thẳng.

### Quản lý phiên (Session Management)

- **Persistence**: Tự động lưu Cookie khi trình duyệt đóng và nạp lại khi khởi động để duy trì trạng thái đăng nhập.

### 4.1. Kỹ thuật giả lập con người (Human Simulation)
- **Human-like Typing**: Sử dụng hàm `human_type()` để gõ từ khóa từng phím một với tốc độ và khoảng nghỉ ngẫu nhiên, mô phỏng hành vi suy nghĩ khi gõ của người thật.
- **Modern Pagination**: Hỗ trợ đồng thời cả nút "Next" (đa ngôn ngữ Anh/Việt) và cơ chế **Continuous Scroll** (Cuộn vô tận) mới của Google.
- **Captcha Handling**: Cơ chế `check_captcha()` tự động phát hiện màn hình xác minh và tạm dừng kịch bản, chờ người dùng giải tay trên trình duyệt trước khi tự động chạy tiếp.


## 5. Hệ thống Kịch bản (Scripting Engine)

Hệ thống cho phép chạy bot theo các kịch bản tùy chỉnh thay vì chỉ chạy ngẫu nhiên.

### Cấu trúc kịch bản (JSON)
Mỗi kịch bản là một mảng các bước hành động:
- `search_google`: `{ "type": "search_google", "keyword": "..." }`
- `click_domain`: `{ "type": "click_domain", "domain": "...", "max_pages": 5 }`
- `goto`: `{ "type": "goto", "url": "..." }`
- `simulate_reading`: `{ "type": "simulate_reading", "min": 60, "max": 180 }`
- `scroll`: `{ "type": "scroll" }`
- `click_internal`: `{ "type": "click_internal", "count": 2 }`
- `wait`: `{ "type": "wait", "seconds": 10 }`

### Trình soạn thảo trực quan (Script Editor)
Hệ thống cung cấp giao diện quản lý và soạn thảo kịch bản dành cho người không rành code:
- **Tự động dịch JSON**: Hiển thị các bước dưới dạng ngôn ngữ tự nhiên (tiếng Việt).
- **Kéo thả**: Hỗ trợ sắp xếp thứ tự các bước bằng thao tác kéo thả trong ListWidget.
- **Form nhập liệu**: Điền thông số hành động thông qua các ô nhập liệu (LineEdit) thay vì viết code.

### Giải quyết xung đột Asyncio (Technical Note)
Để Playwright Sync API hoạt động ổn định trong môi trường PySide6/Qt (vốn có event loop ngầm), hệ thống sử dụng cơ chế:
```python
import asyncio
def start_playwright():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return sync_playwright().start()
```
Điều này đảm bảo mỗi luồng worker có một môi trường async sạch, tránh lỗi `Greenlet.switch()` hoặc `asyncio loop detection`.


## 6. Hướng dẫn thiết lập môi trường (Setup)

Hệ thống nên được chạy trong môi trường ảo (venv) để đảm bảo tính ổn định:

### Khởi tạo và Kích hoạt
1. **Tạo venv**: `python -m venv venv`
2. **Kích hoạt (Windows)**: `.\venv\Scripts\activate`
3. **Cài đặt thư viện**: `pip install -r requirements.txt`

### Chạy chương trình
Sau khi kích hoạt venv, chạy:
`python main.py`

## 7. Chiến lược phát triển SEO & AIO (AI Optimization)

Hệ thống được định hướng không chỉ để tăng traffic Google mà còn để lọt vào mắt xanh của các AI (ChatGPT, Gemini).

### Tối ưu Google SEO (Hành vi người dùng)
- **Đa dạng hóa hành vi**: Kịch bản bot cần kết hợp "Dwell time" (ở lại trang lâu), "Bounce rate" (thoát nhanh) và tương tác cuộn/click ngẫu nhiên để tự nhiên nhất.
- **Mô phỏng Customer Journey**: Bot nên tìm kiếm các từ khóa liên quan, truy cập đối thủ, sau đó mới tìm kiếm và click vào website mục tiêu.
- **Social Signals**: Cần phát triển thêm tính năng đăng nhập và click link từ các nền tảng mạng xã hội (Facebook, Reddit, Twitter).

### Tối ưu AI (AIO)
AI đánh giá dựa trên **Chất lượng dữ liệu** và **Độ uy tín (Mentions)**, không phải lượt click.
- **Bot Seeding**: Bot cần tự động tạo tài khoản và đăng bài trên Reddit, Quora, Web 2.0 có chứa nội dung thảo luận tự nhiên (tạo bằng AI) nhắc đến thương hiệu/URL.
- **Data Scraper**: Thu thập bài viết Top 1-10 của đối thủ để dùng API (ChatGPT/Gemini) phân tích cấu trúc, giúp tạo ra content xịn hơn, nhiều entity và data (bảng biểu) hơn.
- **AI Prompt Manipulation**: Dùng bot đăng nhập vào các tài khoản AI miễn phí, liên tục đặt câu hỏi có nhắc đến thương hiệu để mớm dữ liệu vào "Context window" của AI.

## 8. Lộ trình phát triển (Roadmap)

### Giai đoạn 1: Hoàn thiện Lõi (Core)
- [x] Tối ưu hóa Anti-detect engine (WebRTC, Canvas, WebGL, Screen Resolution).
- [x] Tối ưu hiệu suất luồng, tự động hóa tương tác cơ bản (chuột, cuộn, click).
- [x] Xây dựng cơ chế Dwell Time (Mô phỏng đọc) và Bounce Rate tự nhiên.
- [x] **Phát triển Hệ thống Kịch bản (Scripting Engine) & Trình soạn thảo trực quan.**
- [x] **Hiện đại hóa giao diện (Light Mode, Quản lý profile chuyên nghiệp).**
- [ ] Tích hợp API cho các nhà cung cấp Proxy dân cư (Residential Proxies) chất lượng cao.


### Giai đoạn 2: Tự động hóa Nội dung & Seeding
- [ ] Tích hợp API OpenAI (ChatGPT) / Google (Gemini) vào mã nguồn.
- [ ] Xây dựng Module **Context Builder Bot**: Tự động viết và đăng bài lên mạng lưới Web 2.0 / Forums để tăng độ phủ thương hiệu.
- [ ] Mở rộng kịch bản Customer Journey cho Bot Traffic.

### Giai đoạn 3: Hệ thống phân tích Entity
- [ ] Cào dữ liệu (Scraping) đối thủ.
- [ ] Quét và đánh giá cấu trúc dữ liệu (Schema.org, JSON-LD) của trang web mục tiêu để đảm bảo chuẩn "thức ăn" cho AI.

---
*Cập nhật lần cuối: 08/05/2026 bởi Antigravity*
