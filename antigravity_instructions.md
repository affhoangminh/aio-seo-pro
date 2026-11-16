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

- **Persistence**: Tự động lưu Cookie khi trình## 3. Hệ thống Lập lịch & Chiến dịch (Campaign Scheduling)
- **Kiến trúc tập trung:** Chuyển đổi từ gán kịch bản vào Profile sang quản lý theo Chiến dịch (Schedules). Một chiến dịch bao gồm: Profile thực hiện, Chuỗi kịch bản, Thời gian chạy, và Số ngày duy trì.
- **Cơ chế Failover (Dự phòng):**
    - `Specific`: Chạy đúng Profile được chỉ định.
    - `Random`: Chọn ngẫu nhiên 1 Profile trong danh sách để đa dạng hóa dấu vân tay.
    - `Fallback`: Nếu Profile chính gặp lỗi Proxy/Network, hệ thống tự động điều phối Profile dự phòng.
- **Sequence Scripting:** Hỗ trợ chạy nhiều Script nối tiếp nhau trong một phiên. Giữa các Script có thời gian nghỉ (`delay`) tùy chỉnh để mô phỏng hành trình khách hàng phức tạp.
- **Auto-Cleanup:** Sau khi hoàn thành chuỗi kịch bản, hệ thống phải thực hiện `save_cookies()` và `close_browser()` tự động để giải phóng tài nguyên.

## 4. Nguyên tắc UI/UX Modern
- **Card-style Design:** Sử dụng các thẻ (Cards) có viền mỏng và shadow nhẹ thay vì bảng danh sách thô sơ.
- **Interactive Feedback:** Mọi hành động (Lưu, Chạy, Xóa) phải có phản hồi thị giác (Hover effects, Progress indicators).
- **Compact & Clean:** Sử dụng Font-size từ 11px - 13px, viết tắt đơn vị (ví dụ: 'm' thay cho 'phút') để giao diện gọn gàng nhưng vẫn đủ thông tin.
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

## 9. Các thay đổi và tối ưu hóa hệ thống gần đây (Tháng 06/2026)

### 9.1. Khắc phục lỗi đa luồng (Cooperative Shutdown)
- **Vấn đề:** Khi tắt chương trình, luồng chính hoặc luồng dọn dẹp Qt gọi trực tiếp `c.close()` lên các context của luồng worker gây ra lỗi xung đột luồng `Greenlet.switch() returned NULL` và các warning coroutine chưa được await.
- **Giải pháp:** Chuyển sang mô hình tắt hợp tác. Thêm cờ sự kiện thread-safe `shutdown_event = threading.Event()` vào `browser_pool.py`. Hàm `close_all()` chỉ kích hoạt cờ này. Các luồng worker trong `browser_launcher.py` sẽ tự động thoát vòng lặp chờ và gọi `playwright_inst.stop()` dọn dẹp tài nguyên một cách an toàn trong khối `finally` trên chính luồng của nó.

### 9.2. Sửa lỗi Timeout 30 giây khi mở trình duyệt
- **Vấn đề:** Lệnh `context.wait_for_event("close")` mặc định có thời gian chờ là 30 giây (30000ms). Nếu người dùng không đóng trình duyệt trong 30 giây, trình duyệt sẽ tự động crash/đóng do ném lỗi TimeoutError.
- **Giải pháp:** Thay thế bằng một vòng lặp kiểm tra sự kiện đóng với timeout ngắn (1000ms) kết hợp kiểm tra trạng thái tắt ứng dụng (`is_shutdown()`). Trình duyệt sẽ luôn mở ổn định cho đến khi người dùng chủ động đóng.

### 9.3. Đồng bộ Cookie & Xử lý ngoại lệ
- **Cookie:** Sửa lỗi sai lệch tên file cookie giữa lưu và tải (lưu dùng định dạng `cookies_{profile_id}.json` nhưng tải lại tìm `{profile_id}.json`). Cả hai đã được đồng bộ sử dụng `cookies_{profile_id}.json`.
- **Ngoại lệ:** Bỏ qua lỗi context đã đóng khi gọi `context.cookies()` trong sự kiện close vì trình duyệt persistent context đã tự lưu cache và session hoàn chỉnh vào đĩa. Đồng thời, đăng ký thêm sự kiện lưu cookie khi đóng tab/page để backup cookie khi context vẫn còn sống.

### 9.4. Kịch bản gõ chữ mô phỏng người thật (`type_text`)
- **Bộ máy:** Thêm hành động `"type_text"` hỗ trợ tìm kiếm selector, gõ từng ký tự với tốc độ biến thiên ngẫu nhiên và nhấn `Enter`. Nếu `selector` trống, bot tự động gõ trực tiếp vào vị trí con trỏ/focus hiện tại của trang (rất hữu ích cho các trang tự động focus như Claude, ChatGPT hay Google).
- **Giao diện soạn thảo:** Tích hợp trực quan hành động **"Gõ văn bản & Enter"** vào `ScriptEditorDialog` giúp người dùng cấu hình dễ dàng mà không cần viết JSON.

### 9.5. Tự động phát hiện và tạm dừng chờ giải xác minh bảo mật (Cloudflare/DDoS)
- Thêm bộ lọc nhận diện các trang bảo vệ của Cloudflare, DDoS, Akamai trong hàm `check_captcha()`.
- Khi phát hiện màn hình xác minh, kịch bản tự động dừng, hướng dẫn người dùng giải tay hoặc chờ hệ thống xác minh. Ngay sau khi giải xong và nội dung bảo vệ biến mất, bot tự động tiếp tục kịch bản.

### 9.6. Sửa lỗi Unicode Encode trên Windows Console
- Cấu hình lại mã hóa đầu ra tiêu chuẩn (`sys.stdout` và `sys.stderr`) thành `UTF-8` tại điểm đầu chương trình (`main.py` và các script chạy thử) để triệt tiêu lỗi biên dịch `'charmap' codec can't encode character` khi in các biểu tượng emoji ra terminal Windows.

---
*Cập nhật lần cuối: 09/06/2026 bởi Antigravity*

