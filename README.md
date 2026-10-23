# 🎧 Lossless Player

Một ứng dụng web **một trang** (HTML/CSS/JS, không cần build) để **tìm và nghe nhạc lossless (FLAC) hợp pháp** từ [Internet Archive](https://archive.org) (bao gồm Live Music Archive / etree). Ứng dụng có **bộ xử lý âm thanh Web Audio**.

**Dùng ngay:** https://2n7jn6y6fm-stack.github.io/lossless-player/

## Tính năng
- Tìm album/bộ sưu tập có file FLAC; lọc theo bộ sưu tập (ví dụ `etree`, `opensource_audio`).
- Trình phát có hàng đợi, trộn bài, lặp lại, tua, phím tắt, điều khiển trên màn hình khoá (Media Session).
- Hiển thị định dạng thật của file FLAC: tần số mẫu, bit depth, số kênh, bitrate, đọc từ STREAMINFO.
- **Bộ xử lý âm thanh:**
  - EQ 10 băng (31 Hz – 16 kHz) với các preset.
  - Preamp.
  - Bass enhancer.
  - Compressor/Limiter.
  - Độ rộng stereo.
  - Reverb.
  - Phân tích phổ.
  - Bypass (nút **B**).
- Mọi cài đặt được lưu trong trình duyệt (localStorage).
- Giao diện tối, tiếng Việt, tối ưu cho điện thoại; có thể cài như ứng dụng (PWA).

## 📱 Thêm vào màn hình chính iPhone
1. Mở **Safari** (không dùng Chrome hay app khác) và vào https://2n7jn6y6fm-stack.github.io/lossless-player/
2. Nhấn nút **Chia sẻ** (ô vuông có mũi tên ↑) ở thanh dưới.
3. Kéo xuống và chọn **"Thêm vào MH chính"** (Add to Home Screen), rồi nhấn **Thêm**.
4. Mở app từ biểu tượng 🎧 **Lossless** trên màn hình chính. App chạy toàn màn hình như ứng dụng thật.
5. Lần đầu, **chạm vào màn hình hoặc nút ▶** để iOS cho phép phát âm thanh.

> Mẹo: nếu không nghe thấy tiếng, kiểm tra nút gạt im lặng và âm lượng phần cứng. Trên iOS, thanh âm lượng trong app không có tác dụng; hãy dùng nút âm lượng của máy.

### Chế độ nghe nền (iPhone)
Khi khoá màn hình, iOS tạm dừng Web Audio, nên nhạc qua bộ xử lý sẽ bị ngắt. Mục **"📱 Chế độ nghe nền (iPhone)"** trong phần Bộ xử lý âm thanh có ba lựa chọn:
- **Tự động** (mặc định trên iPhone):
  - Khi app bị ẩn hoặc màn hình khoá, nhạc được chuyển sang một trình phát thường ở **đúng vị trí đang nghe**, nên vẫn tiếp tục phát.
  - Khi mở lại app, nhạc tự quay về bộ xử lý. Nếu iOS chưa cho phép, chỉ cần chạm vào màn hình một lần.
- **Luôn bật:** luôn phát trực tiếp, ổn định nhất khi nghe lâu với màn hình tắt, nhưng **không có EQ/hiệu ứng**.
- **Tắt:** luôn dùng bộ xử lý. Nhạc có thể dừng khi khoá màn hình.

Giới hạn:
- Trong lúc phát nền, EQ và hiệu ứng **không áp dụng**.
- Có thể có khoảng lặng ngắn (dưới 1 giây) khi chuyển.
- Trình phát nền chỉ hoạt động sau khi bạn đã chạm vào app ít nhất một lần.

## Chạy trên máy tính (tuỳ chọn)
Chỉ cần mở `index.html` qua bất kỳ web server tĩnh nào. Ứng dụng tự kết nối trực tiếp tới archive.org, vì archive.org cho phép CORS.

Có kèm `server.py`, một proxy cục bộ tuỳ chọn (Python 3, không cần thư viện ngoài):
```bash
python3 server.py      # mở http://localhost:8080
```
Khi chạy qua `server.py`, app tự dùng chế độ "Proxy cục bộ". Có thể đổi chế độ trong phần Thông tin.

## Nguồn nhạc & bản quyền
Ứng dụng chỉ dùng API công khai của Internet Archive (`advancedsearch`, `metadata`, `download`) và chỉ liệt kê file FLAC công khai. Hãy tôn trọng giấy phép của từng bản ghi (xem liên kết "Trang gốc").
