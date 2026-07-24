"""สร้างไอคอนปุ่มเครื่องมือทั้งชุด (PNG โปร่งใส 64x64) ลง ui/_shared/icon/

ทำไมต้องมี: ฟอนต์ Kanit (และ Noto ของ pygame_gui) **ไม่มี glyph อีโมจิเลย**
→ ปุ่มเครื่องมือที่ใช้ตัวอักษร 🔗 〰️ 🧲 🤖 ฯลฯ เรนเดอร์ออกมาเป็น "กล่องสี่เหลี่ยม (tofu)" ทั้งแถบ
(ยืนยันด้วยการเทียบพิกเซลกับ .notdef ของฟอนต์)
theme_manager.load_icon() หาไฟล์จาก ui/<theme>/icon/ → ui/_shared/icon/ → iconpho/
วางไว้ที่ _shared จึงใช้ได้ทุกธีม

รันซ้ำได้: python tools/make_icons.py
"""
import os
import math
import pygame

pygame.init()

S = 64                              # ขนาดไฟล์ (ตอนใช้จริงถูก smoothscale ลงเป็น 30px)
OUT = os.path.join("ui", "_shared", "icon")

FG = (232, 236, 242)                # เส้นหลัก — สว่าง (ปุ่มพื้นเข้ม)
DIM = (150, 158, 170)               # เส้นรอง
ACC = (120, 200, 255)               # สีเน้น (ฟ้า)
WARN = (255, 120, 120)              # แดง (ลบ)
ROPE = (190, 160, 110)              # เชือก — น้ำตาล (ตรงกับ colors.LINK_ROPE)
SHOCK_BODY = (150, 150, 156)        # โช้ค — กระบอกเทา (ตรงกับ colors.LINK_SHOCK)
SHOCK_ROD = (95, 95, 105)           # โช้ค — ก้านสูบเทาเข้ม (ตรงกับ colors.LINK_SHOCK_ROD)
GREEN = (120, 220, 140)


def new():
    return pygame.Surface((S, S), pygame.SRCALPHA)


def save(surf, name):
    os.makedirs(OUT, exist_ok=True)
    pygame.image.save(surf, os.path.join(OUT, name))
    print("  ✔", name)


# ---------------------------------------------------------------- Spawn Block
s = new()
pygame.draw.rect(s, GREEN, (14, 14, 36, 36), border_radius=4)
pygame.draw.rect(s, FG, (14, 14, 36, 36), 3, border_radius=4)
pygame.draw.line(s, FG, (32, 24), (32, 40), 3)      # +
pygame.draw.line(s, FG, (24, 32), (40, 32), 3)
save(s, "Spawn Block.png")

# --------------------------------------------------------------- spawn target
s = new()
for r, col in ((24, FG), (16, WARN), (8, FG)):
    pygame.draw.circle(s, col, (32, 32), r, 3)
pygame.draw.circle(s, WARN, (32, 32), 3)
save(s, "spawn target.png")

# ---------------------------------------------------------------------- Glue
s = new()  # แม่เหล็กเกือกม้า
pygame.draw.arc(s, WARN, (12, 10, 40, 40), math.pi, 2 * math.pi, 8)
pygame.draw.rect(s, WARN, (12, 30, 8, 18))
pygame.draw.rect(s, WARN, (44, 30, 8, 18))
pygame.draw.rect(s, FG, (12, 44, 8, 8))
pygame.draw.rect(s, FG, (44, 44, 8, 8))
save(s, "Glue.png")

# -------------------------------------------------------------------- Spring
s = new()  # ซิกแซก 2D
pts = [(10, 32)]
for i in range(6):
    x = 14 + i * 6.5
    pts.append((x, 16 if i % 2 == 0 else 48))
pts.append((54, 32))
pygame.draw.lines(s, FG, False, pts, 4)
pygame.draw.circle(s, FG, (10, 32), 4)
pygame.draw.circle(s, FG, (54, 32), 4)
save(s, "Spring.png")

# ---------------------------------------------------------------------- Rope
s = new()  # เส้นโค้งหย่อน (catenary)
pts = [(8 + i, 18 + 26 * math.sin(math.pi * i / 48.0)) for i in range(49)]
pygame.draw.lines(s, ROPE, False, pts, 5)
pygame.draw.circle(s, FG, (8, 18), 4)
pygame.draw.circle(s, FG, (56, 18), 4)
save(s, "Rope.png")

# --------------------------------------------------------------------- Shock
s = new()  # โช้ค 1D: กระบอกเทา + ก้านสูบเทาเข้ม + หูยึด (ให้ตรงกับที่วาดบนแคนวาส)
pygame.draw.line(s, SHOCK_ROD, (32, 8), (32, 56), 6)          # ก้านสูบ
pygame.draw.rect(s, SHOCK_BODY, (22, 26, 20, 26), border_radius=3)   # กระบอก
pygame.draw.rect(s, SHOCK_ROD, (22, 26, 20, 26), 3, border_radius=3)
pygame.draw.circle(s, SHOCK_ROD, (32, 9), 6, 3)               # หูยึดบน
pygame.draw.circle(s, SHOCK_ROD, (32, 55), 6, 3)              # หูยึดล่าง
pygame.draw.line(s, ACC, (10, 32), (18, 32), 2)               # เครื่องหมายแกน (1 มิติ)
pygame.draw.line(s, ACC, (46, 32), (54, 32), 2)
save(s, "Shock.png")

# ---------------------------------------------------------------------- Path
s = new()  # เส้นทาง waypoint
pts = [(12, 50), (26, 26), (42, 40), (54, 14)]
pygame.draw.lines(s, ACC, False, pts, 3)
for p in pts:
    pygame.draw.circle(s, FG, p, 5)
    pygame.draw.circle(s, ACC, p, 5, 2)
save(s, "Path.png")

# --------------------------------------------------------------- Select tool
s = new()  # ลูกศรเคอร์เซอร์
pygame.draw.polygon(s, FG, [(18, 10), (18, 50), (28, 40), (34, 54), (42, 50), (36, 36), (48, 34)])
pygame.draw.polygon(s, (40, 44, 52),
                    [(18, 10), (18, 50), (28, 40), (34, 54), (42, 50), (36, 36), (48, 34)], 2)
save(s, "Select tool.png")

# --------------------------------------------------------------------- Ruler
s = new()  # ไม้บรรทัดสามเหลี่ยม
pygame.draw.polygon(s, FG, [(10, 52), (54, 52), (10, 12)], 3)
for i in range(1, 5):                                # ขีดสเกล
    x = 10 + i * 9
    pygame.draw.line(s, DIM, (x, 52), (x, 44), 2)
save(s, "Ruler.png")

# -------------------------------------------------------------------- Delete
s = new()  # ถังขยะ
pygame.draw.rect(s, WARN, (18, 20, 28, 32), 3, border_radius=3)
pygame.draw.line(s, WARN, (12, 18), (52, 18), 4)
pygame.draw.rect(s, WARN, (26, 10, 12, 6), 3)
for x in (26, 32, 38):
    pygame.draw.line(s, WARN, (x, 26), (x, 46), 2)
save(s, "Delete.png")

# --------------------------------------------------------------------- Graph
s = new()  # แกน + เส้นกราฟ
pygame.draw.line(s, DIM, (12, 10), (12, 52), 3)
pygame.draw.line(s, DIM, (12, 52), (54, 52), 3)
pygame.draw.lines(s, ACC, False, [(14, 44), (24, 30), (34, 38), (44, 16), (52, 22)], 4)
save(s, "Graph.png")

# ------------------------------------------------------------------------ AI
s = new()  # หุ่นยนต์
pygame.draw.rect(s, FG, (14, 22, 36, 28), 3, border_radius=6)
pygame.draw.circle(s, ACC, (24, 34), 4)
pygame.draw.circle(s, ACC, (40, 34), 4)
pygame.draw.line(s, FG, (26, 44), (38, 44), 3)
pygame.draw.line(s, FG, (32, 12), (32, 22), 3)       # เสาอากาศ
pygame.draw.circle(s, ACC, (32, 10), 4)
pygame.draw.line(s, FG, (8, 32), (14, 32), 3)        # หู
pygame.draw.line(s, FG, (50, 32), (56, 32), 3)
save(s, "AI.png")

print("\nสร้างไอคอนครบ 12 ไฟล์ →", OUT)
