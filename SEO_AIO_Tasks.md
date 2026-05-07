# Checklist Phát Triển AIO SEO PRO (SEO & AIO)

Dưới đây là danh sách chi tiết các công việc cần thực hiện để biến AIO SEO PRO thành một công cụ tối ưu hóa SEO và AIO (AI Optimization) toàn diện.

## GIAI ĐOẠN 1: Nâng cấp Lõi Traffic (Tối ưu Google SEO)
**Mục tiêu:** Làm cho Bot hành xử không thể phân biệt được với người thật.

### 1.1. Hành vi "Đọc hiểu" (Dwell Time & Bounce Rate)
- [x] Tích hợp hàm `simulate_reading()` trong `bot/page_actions.py` để bot ở lại trang 3-5 phút.
- [x] Giả lập hành vi bôi đen văn bản ngẫu nhiên khi đang đọc.
- [x] Tích hợp hàm `simulate_bounce()` với tỷ lệ thoát trang nhanh (20%) để tự nhiên hóa chỉ số Google Analytics.

### 1.2. Mô phỏng "Hành trình khách hàng" (Customer Journey)
- [ ] Cập nhật `bot/google_search_bot.py` để nhận danh sách từ khóa phụ.
- [ ] Cấu hình kịch bản: Tìm từ khóa phụ -> Click Top 3 đối thủ -> Quay lại Google -> Tìm từ khóa chính -> Click website của bạn.

### 1.3. Tín hiệu Mạng Xã Hội (Social Signals)
- [ ] Tạo module `bot/social_traffic_bot.py`.
- [ ] Viết kịch bản tự động đăng nhập & lưu Session cho Facebook, Reddit, X (Twitter).
- [ ] Kịch bản click link Referral từ mạng xã hội về website chính.

### 1.4. Nâng cấp Anti-detect
- [ ] Hỗ trợ cấu hình tích hợp API xoay IP cho Proxy Dân cư (Residential Proxy).

---

## GIAI ĐOẠN 2: Tự động hóa Nội dung & Seeding (Tối ưu AIO)
**Mục tiêu:** Phủ sóng thương hiệu để huấn luyện AI (ChatGPT, Gemini).

### 2.1. Tích hợp Trí Tuệ Nhân Tạo (LLM)
- [ ] Tạo thư mục `aio_tools/` và file `aio_tools/llm_client.py`.
- [ ] Tích hợp API OpenAI / Gemini để tự động tạo nội dung comment, bài viết seeding.

### 2.2. Context Builder Bot (Bot Seeding Không Spam)
- [ ] Tạo module `bot/forum_seeding_bot.py`.
- [ ] Kịch bản auto-register tài khoản trên Web 2.0 (Medium, Quora, Reddit).
- [ ] Tích hợp giải mã Captcha (2Captcha/Anti-Captcha).
- [ ] Tự động đăng bài seeding nhắc đến Tên thương hiệu/URL một cách tự nhiên.

### 2.3. AI Prompt Manipulator (Mớm dữ liệu cho AI)
- [ ] Tạo module `bot/ai_prompt_bot.py`.
- [ ] Đăng nhập tự động vào ChatGPT/Gemini web.
- [ ] Kịch bản hỏi AI về thương hiệu/sản phẩm của bạn để đưa thông tin vào ngữ cảnh (Context window).

---

## GIAI ĐOẠN 3: Cấu trúc & Phân tích Dữ liệu (Entity & Schema)
**Mục tiêu:** Đảm bảo website cung cấp "thức ăn" chuẩn nhất cho bot AI.

### 3.1. Data Scraper (Cào dữ liệu đối thủ)
- [ ] Tạo module `aio_tools/scraper.py`.
- [ ] Trích xuất các thẻ H2, H3, Bảng biểu (Tables), và Danh sách (Lists) từ Top 10 Google.

### 3.2. Content Gap Analyzer
- [ ] Viết prompt đưa dữ liệu scraper vào AI để phân tích điểm yếu của đối thủ.
- [ ] Tự động xuất ra Dàn ý (Outline) bài viết chuẩn SEO & AIO.

### 3.3. Schema Validator (Kiểm tra thực thể)
- [ ] Viết công cụ quét và xác thực JSON-LD / Schema.org của URL mục tiêu.
