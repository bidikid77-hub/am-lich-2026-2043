# Lịch vạn niên 2026–2043

Lịch âm Việt Nam dạng **iCalendar / WebCal** cho giai đoạn **2026–2043**, kèm trang tra cứu hiện đại và dữ liệu JSON để tái tạo lịch.

## Tính năng

- Mỗi ngày dương lịch là một sự kiện nguyên ngày trong `.ics`
- Hiển thị **ngày/tháng/năm âm lịch** theo dạng `dd/mm/yyyy ÂL`
- Với **tháng nhuận**, hiển thị `dd/mm/yyyy ÂLN` để dễ phân biệt
- Có **can chi năm** và **can chi ngày**
- Bao phủ **24 tiết khí**: Lập xuân, Xuân phân, Hạ chí, Thu phân, Đông chí...
- Đánh dấu **Mùng 1**, **Rằm**, và các ngày lễ âm lịch phổ biến
- Gắn nhãn **Hoàng đạo / Hắc đạo** theo quy tắc truyền thống đơn giản
- Có trang tra cứu để xem nhanh theo ngày, tháng, giờ hoàng đạo, sao tốt/xấu, việc nên làm / nên tránh

## Ngày lễ âm lịch có sẵn

- Tết Nguyên Đán
- Rằm tháng Giêng
- Giỗ Tổ Hùng Vương
- Lễ Phật Đản
- Tết Đoan Ngọ
- Vu Lan
- Tết Trung Thu
- Ông Công Ông Táo

## Tệp trong repo

- `index.html` — trang tra cứu
- `am-lich-2026-2043.ics` — file lịch để subscribe trên iPhone / Google Calendar / Outlook
- `lunar_metadata.json` — dữ liệu ngày âm dùng cho giao diện web
- `generate_lunar_ics.py` — script sinh lại dữ liệu và lịch

## Cách dùng

### 1) Xem trực tiếp trên web

Mở `index.html` hoặc GitHub Pages nếu đã bật.

### 2) Thêm vào lịch iPhone

Sau khi bật GitHub Pages, dùng link:

```text
webcal://bidikid77-hub.github.io/am-lich-2026-2043/am-lich-2026-2043.ics
```

Link HTTPS dự phòng:

```text
https://bidikid77-hub.github.io/am-lich-2026-2043/am-lich-2026-2043.ics
```

### 3) Sinh lại lịch

```bash
python3 generate_lunar_ics.py
```

## Kiểm tra nhanh

```bash
python3 - <<'PY'
from pathlib import Path
ics = Path('am-lich-2026-2043.ics').read_text(encoding='utf-8')
print('VEVENT:', ics.count('BEGIN:VEVENT'))
print('VCALENDAR:', 'BEGIN:VCALENDAR' in ics and 'END:VCALENDAR' in ics)
PY
```

## Ghi chú

- Dữ liệu âm lịch và tiết khí được sinh tự động từ Python.
- Nội dung Hoàng đạo / Hắc đạo mang tính tham khảo văn hóa truyền thống.
- Nếu thay đổi logic sinh lịch, nhớ cập nhật lại cả `lunar_metadata.json` và `am-lich-2026-2043.ics`.
