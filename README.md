# Lịch vạn niên 2026-2043

Lịch âm Việt Nam dạng iCalendar/WebCal và trang tra cứu lịch vạn niên hiện đại cho giai đoạn 2026-2043.

## Nội dung

Mỗi ngày dương lịch là một sự kiện nguyên ngày, có:

- Ngày/tháng/năm âm lịch
- Tháng nhuận nếu có
- Can chi năm
- Can chi ngày
- Đầy đủ 24 tiết khí: Lập xuân, Xuân phân, Hạ chí, Thu phân, Đông chí...
- Mùng 1 và ngày rằm 15 âm lịch
- Nhãn Hoàng đạo / Hắc đạo tham khảo theo quy tắc truyền thống đơn giản
- Một số ngày lễ âm lịch phổ biến:
  - Tết Nguyên Đán
  - Rằm tháng Giêng
  - Giỗ Tổ Hùng Vương
  - Tết Đoan Ngọ
  - Vu Lan
  - Tết Trung Thu
  - Ông Công Ông Táo

## Files

- `generate_lunar_ics.py`: script sinh lịch
- `am-lich-2026-2043.ics`: file iCalendar
- `lunar_metadata.json`: dữ liệu ngày âm dạng JSON
- `index.html`: landing page

## Cách sinh lại lịch

```bash
python3 generate_lunar_ics.py
```

## Kiểm tra nhanh

```bash
python3 - <<'PY'
from pathlib import Path
ics = Path('am-lich-2026-2043.ics').read_text(encoding='utf-8')
print('VEVENT', ics.count('BEGIN:VEVENT'))
print('Calendar OK', 'BEGIN:VCALENDAR' in ics and 'END:VCALENDAR' in ics)
PY
```

## Ghi chú

Script dùng thư viện Python `lunardate` để chuyển đổi dương lịch sang âm lịch.
