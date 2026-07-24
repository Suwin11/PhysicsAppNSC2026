# คู่มือปรับ UI (UI_SCALE)

## กฎข้อเดียวที่ต้องจำ

**อย่าเอา `S()` ไปครอบความกว้าง/สูงของหน้าจอ**

```python
R(10, 40, 250, 30)                                     # ✅ layout ล้วน
pygame.Rect(width - S(300), S(45), S(300), h - S(85))  # ✅ ยึดขอบจอ
pygame.Rect(S(width - 300), ...)                       # ❌ ผิด! สเกลความกว้างจอ
```

`width` / `height` เป็นพิกเซลจริงอยู่แล้ว — สเกลเฉพาะ "ตัวเลขคงที่" เท่านั้น

---

## ไฟล์ที่เกี่ยวข้อง

| ไฟล์ | หน้าที่ |
|---|---|
| `ui_scale.py` | **ตัวแปรเดียว** + ตัวช่วย `s()` `R()` `f()` + ค่าคงที่ layout |
| `ui_core.py` | สร้าง UI ทั้งหมด (ผ่าน `S()` / `R()` แล้ว) |
| `main.py` | โหลดสเกลตอนบูต + hit-test + `apply_ui_scale()` |
| `progress.py` | เก็บค่าลง `savegame.json` |
| `check_ui_scale.py` | เกตตรวจ 4 ข้อ (รันคู่กับ `run_checks.py`) |

---

## งานที่ทำบ่อย

### 1. เปลี่ยนสัดส่วนถาวร (ทุกคนเห็นเหมือนกัน)

แก้ `BASE_*` ใน `ui_scale.py` — **ห้ามแก้ใน `build_game_ui`**

```python
BASE_TOP_BAR_H     = 45    # แถบบน
BASE_BOTTOM_BAR_H  = 40    # แถบล่าง
BASE_LEFT_BAR_W    = 66    # แถบเครื่องมือซ้าย
BASE_LEFT_HIT_W    = 60    # ขอบเขต hit-test (main.py ใช้)
BASE_RIGHT_PANEL_W = 300   # Inspector ขวา
BASE_TOOL_BTN      = 40    # ปุ่มเครื่องมือ
BASE_TOOL_ICON     = 30    # ไอคอนในปุ่ม
```

> ⚠️ `BASE_RIGHT_PANEL_W` ถูกอ่านทั้งตอนสร้าง panel **และ** ตอน main.py กันคลิกทะลุ
> แก้ที่เดียวจบ — ถ้าไปแก้แยกกันจะเกิด "โซนคลิกไม่ได้" ที่มองไม่เห็นข้างๆ panel

### 2. ขยับ / เปลี่ยนขนาดของที่มีอยู่

หาใน `build_game_ui` แล้วแก้ตัวเลข **ข้างใน** `S()`

```python
# เดิม
self.elements['btn_menu'] = UIButton(R(5, 5, 80, 35), "MENU", ...)
# อยากให้กว้างขึ้น
self.elements['btn_menu'] = UIButton(R(5, 5, 100, 35), "MENU", ...)
```

### 3. เพิ่มปุ่มใหม่ในแท็บ Phys

ใช้ pattern ตัวแปร `y` ที่ไหลลงมา:

```python
self.elements['btn_mine'] = UIButton(pygame.Rect(S(10), y, S(250), S(30)),
    "ปุ่มใหม่", self.game_manager, container=self.elements['cont_phys']); y += S(40)
```

แล้ว **ต้อง** ไปเพิ่มความสูงพื้นที่เลื่อนด้วย ไม่งั้น scrollbar เพี้ยนเงียบๆ:

```python
self.elements['cont_phys'].set_scrollable_area_dimensions((cw, max(vis_h, S(360))))
#                                                                        ^^^ เพิ่มตรงนี้
```

### 4. เพิ่ม preset ขนาด

เติมใน `PRESETS` ของ `ui_scale.py` — label ในหน้า Settings จะขึ้นชื่อให้เอง

```python
PRESETS = [(0.75,"เล็กมาก"), (0.90,"เล็ก"), (1.00,"ปกติ"),
           (1.25,"ใหญ่"), (1.50,"ใหญ่มาก"), (1.75,"ใหญ่สุด")]
```

---

## เรื่องที่ต้องรู้ก่อนแก้

**แถบบนซ่อนตัวเองตอนที่แคบ** — `build_game_ui` มี fallback ราวบรรทัด 590:

```python
if _avail < S(581):   self.elements['lbl_mem'].hide()          # ซ่อน Mem
if _avail < S(489):   # ซ่อนกลุ่ม scrub เวลาทั้งชุด
```

ที่ 2.0x บนจอ 1600px กลุ่มควบคุมเวลา **จะหายไปเอง** — เป็นพฤติกรรมที่ถูกต้อง
ไม่ใช่บั๊ก แต่ถ้าไม่รู้จะงงว่าปุ่มหายไปไหน

**หน้าต่าง Settings ใช้สเกลของตัวเอง** (`k` ที่ถูกจำกัดด้วยความสูงจอ) ไม่ใช่ `UI_SCALE`
ตรงๆ เพราะถ้าใช้ตรงๆ ที่ 1.5x ปุ่ม CLOSE จะไปอยู่ที่ y=946 บนจอสูง 900px →
สไลเดอร์ปรับขนาดหลุดจอ → กดกลับไม่ได้เลย ต้องไปแก้ `savegame.json` มือ
**ถ้าจะแก้ SettingsWindow ใช้ `_s()` / `_r()` (ตัวเล็ก) เท่านั้น อย่าใช้ `S()` / `R()`**

---

## ⚠️ ส่วนที่ยังไม่ได้สเกล

ไฟล์พวกนี้ยังใช้เลข hardcode อยู่ **แต่ฟอนต์ของมันสเกลตามแล้ว** (เพราะใช้ธีมร่วมกัน)
→ ที่ 1.5x ขึ้นไป **ตัวหนังสือจะล้นกรอบ**

| ไฟล์ | จำนวน `pygame.Rect(` | ความสำคัญ |
|---|---|---|
| `bulk_editor.py` | 29 | สูง (ใช้ `game_manager` ร่วม) |
| `graph_ui.py` | 16 | สูง |
| `geometry_editor.py` | 16 | กลาง |
| `ai_ui.py` | 12 | กลาง |
| `whiteboard.py` | 9 | ต่ำ |
| `ui_calculator.py` | 5 | ต่ำ |

### วิธีแปลงทีละไฟล์ (3 บรรทัด)

```python
# 1. บนหัวไฟล์
from ui_scale import s as S, R

# 2. Rect ที่เป็นเลขล้วน
pygame.Rect(10, 40, 250, 30)   →   R(10, 40, 250, 30)

# 3. Rect ที่ยึดขอบจอ — สเกลเฉพาะค่าคงที่
pygame.Rect(self.width - W - 8, 44, W, self.height - 58)
→ pygame.Rect(self.width - W - S(8), S(44), W, self.height - S(58))
```

แนะนำให้ทำทีละไฟล์ แล้วรัน `run_checks.py` + `check_ui_scale.py` ทุกครั้ง

---

## รันเกตก่อนส่งมอบทุกครั้ง

```bash
python3 run_checks.py        # ต้องได้ 8/8
python3 check_ui_scale.py    # ต้องได้ 4/4
```

`check_ui_scale.py` ตรวจ:
1. ทุกมิติโตตามสเกล (คลาดเคลื่อนได้ 2px จากการปัดเศษ)
2. ฟอนต์โตตามด้วย
3. ที่ 2.0x panel ไม่ล้นจอ / ปุ่ม DELETE ไม่หลุดออกนอก panel
4. กลับมา 1.0 แล้วเท่าเดิมเป๊ะ (ไม่มีค่าค้าง)
