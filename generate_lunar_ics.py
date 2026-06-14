from __future__ import annotations

import json
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from lunardate import LunarDate
import sxtwl

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "am-lich-2026-2043.ics"
META = ROOT / "lunar_metadata.json"
VN = ZoneInfo("Asia/Ho_Chi_Minh")
UTC = ZoneInfo("UTC")
START_YEAR = 2026
END_YEAR = 2043

CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
MONTH_NAMES = ["Giêng", "Hai", "Ba", "Tư", "Năm", "Sáu", "Bảy", "Tám", "Chín", "Mười", "Mười một", "Chạp"]
WEEKDAYS = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
TRUC = ["Kiến", "Trừ", "Mãn", "Bình", "Định", "Chấp", "Phá", "Nguy", "Thành", "Thu", "Khai", "Bế"]
NHI_THAP_BAT_TU = ["Giác", "Cang", "Đê", "Phòng", "Tâm", "Vĩ", "Cơ", "Đẩu", "Ngưu", "Nữ", "Hư", "Nguy", "Thất", "Bích", "Khuê", "Lâu", "Vị", "Mão", "Tất", "Chủy", "Sâm", "Tỉnh", "Quỷ", "Liễu", "Tinh", "Trương", "Dực", "Chẩn"]

FESTIVALS = {(1, 1): "Tết Nguyên Đán", (1, 15): "Rằm tháng Giêng", (3, 10): "Giỗ Tổ Hùng Vương", (5, 5): "Tết Đoan Ngọ", (7, 15): "Vu Lan", (8, 15): "Tết Trung Thu", (12, 23): "Ông Công Ông Táo"}
SOLAR_TERMS = {0:"Đông chí",1:"Tiểu hàn",2:"Đại hàn",3:"Lập xuân",4:"Vũ thủy",5:"Kinh trập",6:"Xuân phân",7:"Thanh minh",8:"Cốc vũ",9:"Lập hạ",10:"Tiểu mãn",11:"Mang chủng",12:"Hạ chí",13:"Tiểu thử",14:"Đại thử",15:"Lập thu",16:"Xử thử",17:"Bạch lộ",18:"Thu phân",19:"Hàn lộ",20:"Sương giáng",21:"Lập đông",22:"Tiểu tuyết",23:"Đại tuyết"}
HOANG_DAO_HOURS = {
    "Tý": ["Tý", "Sửu", "Mão", "Ngọ", "Thân", "Dậu"], "Ngọ": ["Tý", "Sửu", "Mão", "Ngọ", "Thân", "Dậu"],
    "Sửu": ["Dần", "Mão", "Tỵ", "Thân", "Tuất", "Hợi"], "Mùi": ["Dần", "Mão", "Tỵ", "Thân", "Tuất", "Hợi"],
    "Dần": ["Tý", "Sửu", "Thìn", "Tỵ", "Mùi", "Tuất"], "Thân": ["Tý", "Sửu", "Thìn", "Tỵ", "Mùi", "Tuất"],
    "Mão": ["Tý", "Dần", "Mão", "Ngọ", "Mùi", "Dậu"], "Dậu": ["Tý", "Dần", "Mão", "Ngọ", "Mùi", "Dậu"],
    "Thìn": ["Dần", "Thìn", "Tỵ", "Thân", "Dậu", "Hợi"], "Tuất": ["Dần", "Thìn", "Tỵ", "Thân", "Dậu", "Hợi"],
    "Tỵ": ["Sửu", "Thìn", "Ngọ", "Mùi", "Tuất", "Hợi"], "Hợi": ["Sửu", "Thìn", "Ngọ", "Mùi", "Tuất", "Hợi"],
}
HOUR_RANGES = {"Tý":"23:00-01:00", "Sửu":"01:00-03:00", "Dần":"03:00-05:00", "Mão":"05:00-07:00", "Thìn":"07:00-09:00", "Tỵ":"09:00-11:00", "Ngọ":"11:00-13:00", "Mùi":"13:00-15:00", "Thân":"15:00-17:00", "Dậu":"17:00-19:00", "Tuất":"19:00-21:00", "Hợi":"21:00-23:00"}


def ical_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")

def fold(line: str) -> str:
    raw = line.encode("utf-8"); parts=[]
    while len(raw)>75:
        cut=75
        while cut>0 and (raw[cut] & 0b11000000)==0b10000000: cut-=1
        parts.append(raw[:cut].decode("utf-8")); raw=raw[cut:]
    parts.append(raw.decode("utf-8")); return "\r\n ".join(parts)

def gz_text(gz) -> str: return f"{CAN[gz.tg]} {CHI[gz.dz]}"
def can_chi_year(year:int)->str: return f"{CAN[(year+6)%10]} {CHI[(year+8)%12]}"
def lunar_month_name(m:int, leap:bool)->str: return f"Tháng {MONTH_NAMES[m-1]}{' (nhuận)' if leap else ''}"
def is_leap_month(ld:LunarDate)->bool: return bool(getattr(ld,"isLeapMonth",False))
def solar_to_lunar(d:date)->LunarDate: return LunarDate.fromSolarDate(d.year,d.month,d.day)
def solar_term_for_date(d:date)->str|None:
    x=sxtwl.fromSolar(d.year,d.month,d.day)
    return SOLAR_TERMS.get(x.getJieQi()) if x.hasJieQi() else None

def day_quality(ld:LunarDate, day_branch:str, term:str|None)->str:
    score=0
    if ld.day in {1,8,14,15,18,23,26}: score+=1
    if term: score+=1
    if day_branch in {"Tý","Dần","Mão","Ngọ","Mùi","Dậu"}: score+=1
    if ld.day in {4,7,13,18,22,27}: score-=1
    return "Hoàng đạo" if score>=1 else "Hắc đạo"

def truc_for(ld:LunarDate, day_branch_index:int)->str:
    # Practical lookup approximation: rotate by lunar month for compact modern almanac display.
    return TRUC[(day_branch_index - (ld.month-1)) % 12]

def stars_for(quality:str, term:str|None, ld:LunarDate)->tuple[list[str],list[str]]:
    good=[]; bad=[]
    if quality=="Hoàng đạo": good += ["Thiên đức", "Nguyệt đức"]
    else: bad += ["Hắc đạo", "Không vong"]
    if term: good.append(f"Tiết khí {term}")
    if ld.day in {1,15}: good.append("Ngày sóc/vọng")
    if ld.day in {5,14,23}: bad.append("Nguyệt kỵ tham khảo")
    return good, bad

def recommendations(quality:str, truc:str, good:list[str], bad:list[str])->tuple[list[str],list[str],str]:
    yes=[]; no=[]
    if quality=="Hoàng đạo": yes += ["cầu an", "ký kết việc nhỏ", "khai việc nhẹ"]
    else: yes += ["việc thường ngày", "sắp xếp giấy tờ", "dọn dẹp"]
    if truc in {"Thành","Khai","Định","Mãn"}: yes += ["khai trương", "gặp gỡ", "lập kế hoạch"]
    if truc in {"Phá","Nguy","Bế"}: no += ["khởi sự lớn", "động thổ", "cưới hỏi"]
    if "Nguyệt kỵ tham khảo" in bad: no += ["quyết định tài chính lớn"]
    score = (2 if quality=="Hoàng đạo" else 0) + len(good) - len(bad)
    level = "Tốt" if score>=3 else "Trung bình" if score>=1 else "Nên thận trọng"
    return sorted(set(yes)), sorted(set(no)), level

def event(uid:str, day:date, summary:str, description:str)->list[str]:
    now=datetime.now(tz=UTC).strftime("%Y%m%dT%H%M%SZ")
    return ["BEGIN:VEVENT", f"UID:{uid}", f"DTSTAMP:{now}", f"LAST-MODIFIED:{now}", f"DTSTART;VALUE=DATE:{day:%Y%m%d}", f"DTEND;VALUE=DATE:{(day+timedelta(days=1)):%Y%m%d}", f"SUMMARY:{ical_escape(summary)}", f"DESCRIPTION:{ical_escape(description)}", "END:VEVENT"]

def main()->None:
    rows=[]; lines=["BEGIN:VCALENDAR","VERSION:2.0","PRODID:-//Hermes//Van Nien 2026-2043//VI","CALSCALE:GREGORIAN","METHOD:PUBLISH","X-WR-CALNAME:Lịch vạn niên 2026-2043","X-WR-TIMEZONE:Asia/Ho_Chi_Minh","X-PUBLISHED-TTL:PT24H"]
    current=date(START_YEAR,1,1); end=date(END_YEAR,12,31); term_count=0
    while current<=end:
        ld=solar_to_lunar(current); sx=sxtwl.fromSolar(current.year,current.month,current.day)
        year_gz=gz_text(sx.getYearGZ()); month_gz=gz_text(sx.getMonthGZ()); day_gz=gz_text(sx.getDayGZ()); day_branch=CHI[sx.getDayGZ().dz]
        term=solar_term_for_date(current); term_count += 1 if term else 0
        festival=FESTIVALS.get((ld.month,ld.day)); is_new=ld.day==1; is_full=ld.day==15
        quality=day_quality(ld,day_branch,term); truc=truc_for(ld,sx.getDayGZ().dz); constellation=NHI_THAP_BAT_TU[current.toordinal()%28]
        good,bad=stars_for(quality,term,ld); should,avoid,level=recommendations(quality,truc,good,bad)
        hours=[f"{h} ({HOUR_RANGES[h]})" for h in HOANG_DAO_HOURS[day_branch]]
        lunar_label=f"{ld.day:02d}/{ld.month:02d}/{ld.year} ÂL"
        summary=lunar_label
        desc=(f"Âm lịch: {ld.day:02d}/{ld.month:02d}/{ld.year}{' nhuận' if is_leap_month(ld) else ''}\n"
              f"Can chi: năm {year_gz}, tháng {month_gz}, ngày {day_gz}\nTiết khí: {term or 'Không'}\nPhân loại: {quality} - {level}\n"
              f"Trực: {truc}\nNhị thập bát tú: {constellation}\nGiờ hoàng đạo: {', '.join(hours)}\nSao tốt: {', '.join(good) if good else 'Không nổi bật'}\nSao xấu: {', '.join(bad) if bad else 'Không nổi bật'}\n"
              f"Nên làm: {', '.join(should)}\nNên tránh: {', '.join(avoid) if avoid else 'Không có cảnh báo lớn'}")
        if festival: desc += f"\nSự kiện: {festival}"
        row={"solar":current.isoformat(),"weekday":WEEKDAYS[current.weekday()],"lunar":f"{ld.day:02d}/{ld.month:02d}/{ld.year}","leap":is_leap_month(ld),"festival":festival or "","solar_term":term or "","is_new_moon":is_new,"is_full_moon":is_full,"can_chi_year":year_gz,"can_chi_month":month_gz,"can_chi_day":day_gz,"quality":quality,"rating":level,"truc":truc,"nhi_thap_bat_tu":constellation,"good_hours":hours,"good_stars":good,"bad_stars":bad,"should_do":should,"avoid":avoid,"explanation":desc}
        rows.append(row); lines.extend(event(f"vannien-{current.isoformat()}@hermes",current,summary,desc)); current+=timedelta(days=1)
    lines.append("END:VCALENDAR"); OUT.write_text("\r\n".join(fold(x) for x in lines)+"\r\n",encoding="utf-8"); META.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"Wrote {OUT}"); print(f"Days: {len(rows)}"); print(f"Solar terms: {term_count}")

if __name__=="__main__": main()
