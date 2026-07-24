# BUILD NOTES — สร้าง .exe (PyInstaller)

## ปัญหาฟอนต์ไทยบน exe (แก้แล้ว)
**อาการเดิม**: build เป็น .exe แล้วภาษาไทยบน **ปุ่ม/dropdown เป็นกล่อง ▢▢▢** ทั้งที่บน canvas (ชื่อโลก ฯลฯ) ขึ้นไทยได้ปกติ

**สาเหตุ**: canvas ใช้ `pygame.font` (resolve path จาก cwd → เจอ) แต่ pygame_gui resolve font path **relative** จาก `_MEIPASS` (โฟลเดอร์ temp ของ onefile exe) ที่ไม่มี `fonts/` → โหลดฟอนต์ไม่ได้ → fallback เป็นฟอนต์ที่ไม่มี glyph ไทย

## วิธีแก้: bake ฟอนต์ฝังในโค้ด
ฟอนต์ถูกฝังใน **`bundled_fonts.py`** (Kanit-Regular/Bold แบบ gzip+base64). ตอน import จะแตกไฟล์ลง `%TEMP%\newton_physics_fonts\` แล้วเผย **absolute path**:
- `bundled_fonts.KANIT_REGULAR`, `bundled_fonts.KANIT_BOLD`

ไฟล์ที่ใช้ absolute path นี้ (แก้แล้ว):
- `ui_core._pick_theme_file()` → สร้าง `theme_runtime.json` (แทน path ใน theme_kanit.json เป็น absolute)
- `ui_core` add_font_paths loop → absolute
- `thai_font._resolve_source()` → ลอง bundled_fonts ก่อน

**ผลดี**: ไม่ต้องพึ่ง `fonts/` ข้าง exe, ไม่ต้อง `--add-data` ฟอนต์, ใช้ได้ทั้ง onefile/onedir. (Kanit = SIL Open Font License → ฝังในโปรแกรมได้ถูกกฎหมาย)

**สถานะ**: verify บน dev แล้ว (theme_runtime.json เป็น absolute + สร้างปุ่มไทยไม่ crash) — **ยังต้องยืนยันบน .exe จริง** ตอน build ครั้งหน้า

## Checklist ตอน build .exe
1. ต้องมี `bundled_fonts.py` อยู่ในโปรเจกต์ (มีแล้ว)
2. datas ที่ควรใส่ใน .spec (ไฟล์ข้อมูลที่โค้ดอ่านตอนรัน):
   - `theme_kanit.json`, `theme_noto.json` (ถ้ามี)
   - โฟลเดอร์ `ui/` (ธีม/ไอคอน), `iconpho/` (ไอคอนเก่า), `worlds/`
   - `fonts/` ไม่จำเป็นแล้ว (ฟอนต์ bake อยู่ในโค้ด) แต่ใส่ไว้ก็ไม่เสียหาย (thai_font/บาง fallback ยังลองหา)
3. hidden imports ที่อาจต้อง: `pygame_gui`, และถ้า pygame_gui หา data ของตัวเองไม่เจอให้เพิ่ม `--collect-data pygame_gui`
4. ทดสอบหลัง build: เปิด exe → เข้าโลก → ดูปุ่ม/dropdown ว่าเป็นภาษาไทย (ไม่ใช่กล่อง)
5. ถ้ายังเป็นกล่อง: เช็ค `%TEMP%\newton_physics_fonts\theme_runtime.json` ว่ามี + path ข้างในเป็น absolute จริง

## หมายเหตุ
- ผู้ใช้ใส่ diagnostic preamble หัว `main.py` (เขียน `debug_log.txt`) — เช็ค working dir/ฟอนต์ตอนเปิด มีประโยชน์ตอน debug build **อย่าลบ**
- `run_checks.py` = smoke test รันก่อนส่ง/ก่อน build ทุกครั้ง (ผ่าน = exit 0)
