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
- **Canvas Noise**: Thêm nhiễu ngẫu nhiên vào dữ liệu điểm ảnh (Pixel data) của Canvas. Mỗi Profile có một mã nhiễu riêng (`canvas_noise`).
- **WebGL Spoofing**: Giả lập Card đồ họa (Vendor/Renderer) theo đúng cấu hình Profile (ví dụ: NVIDIA, Intel, AMD).
- **Screen Consistency**: Ép các thông số `screen.width`, `window.innerWidth` phải khớp chính xác với độ phân giải giả lập, tránh bị phát hiện do sự lệch lạc thông số.

## 3. Tối ưu hóa hiệu suất (Performance Optimization)

### Chiến lược tải trang (Loading Strategy)
- **Wait Until**: Sử dụng `wait_until="domcontentloaded"` thay vì `load`. Trình duyệt sẽ bắt đầu xử lý Bot ngay khi khung trang web hiện ra, không đợi tải các tài nguyên rác.
- **HTTP/2**: Luôn bật HTTP/2 để tận dụng khả năng tải dữ liệu song song, giúp tốc độ tải trang nhanh gấp 2-3 lần.
- **Resource Blocking**: Hỗ trợ cơ chế chặn Image/Media/Font (tùy chọn) để tiết kiệm băng thông Proxy.

## 4. Cơ chế Bot & Multi-tab

### Xoay vòng Tab (Tab Rotation)
- **Logic**: Chương trình có khả năng mở nhiều Tab cùng lúc và thực hiện xoay vòng (`bring_to_front`).
- **Human Behavior**: Sau mỗi lần chuyển Tab, Bot thực hiện cuộn trang (`mouse.wheel`) và nghỉ ngơi (`random_sleep`) để giả lập hành vi đa nhiệm của người dùng thật.

### Điều khiển chuột (Mouse AI)
- Di chuyển chuột theo quỹ đạo bước (steps) với tốc độ biến thiên, không di chuyển tức thời theo đường thẳng.

## 5. Quản lý dữ liệu (Data Management)

- **Cookie Isolation**: Mỗi Profile lưu dữ liệu trong một thư mục riêng (`browser_profiles/profile_ID`).
- **Persistence**: Tự động lưu Cookie khi trình duyệt đóng và nạp lại khi khởi động để duy trì trạng thái đăng nhập.

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
- [ ] Tích hợp API cho các nhà cung cấp Proxy dân cư (Residential Proxies) chất lượng cao.

### Giai đoạn 2: Tự động hóa Nội dung & Seeding
- [ ] Tích hợp API OpenAI (ChatGPT) / Google (Gemini) vào mã nguồn.
- [ ] Xây dựng Module **Context Builder Bot**: Tự động viết và đăng bài lên mạng lưới Web 2.0 / Forums để tăng độ phủ thương hiệu.
- [ ] Mở rộng kịch bản Customer Journey cho Bot Traffic.

### Giai đoạn 3: Hệ thống phân tích Entity
- [ ] Cào dữ liệu (Scraping) đối thủ.
- [ ] Quét và đánh giá cấu trúc dữ liệu (Schema.org, JSON-LD) của trang web mục tiêu để đảm bảo chuẩn "thức ăn" cho AI.

---
*Cập nhật lần cuối: 07/05/2026 bởi Antigravity*
