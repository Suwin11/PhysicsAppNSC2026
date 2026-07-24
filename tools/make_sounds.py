"""สร้างเสียงชนตัวอย่าง 3 ไฟล์ (.wav) ไว้ในโฟลเดอร์ sound/

เป็นแค่ "ตัวอย่างให้ใช้ได้ทันที" — ลบทิ้งแล้วเอาไฟล์ของตัวเองมาวางแทนได้เลย
(โฟลเดอร์ sound/ รับ .wav .ogg .mp3 .flac กี่ไฟล์ก็ได้ ชื่ออะไรก็ได้)

รัน:  python tools/make_sounds.py
"""
import os, math, wave, struct, random

SR = 44100
OUT = "sound"
os.makedirs(OUT, exist_ok=True)

def write(name, samples):
    path = os.path.join(OUT, name)
    with wave.open(path, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, s)) * 32000)) for s in samples))
    print("  ✔", path)

def env(i, n, attack=0.002, decay=1.0):
    t = i / SR
    a = min(1.0, t / attack) if attack > 0 else 1.0
    return a * math.exp(-t / decay)

random.seed(3)

# 1) thud — ตุ้บทึบ (โทนต่ำ + นอยส์นิดหน่อย)
n = int(SR * 0.28); s = []
for i in range(n):
    t = i / SR
    tone = math.sin(2*math.pi*95*t) * 0.7 + math.sin(2*math.pi*150*t) * 0.25
    noise = random.uniform(-1, 1) * 0.25 * math.exp(-t / 0.02)
    s.append((tone + noise) * env(i, n, 0.001, 0.055))
write("impact_thud.wav", s)

# 2) knock — เคาะไม้ (โทนกลาง สั้น)
n = int(SR * 0.18); s = []
for i in range(n):
    t = i / SR
    tone = (math.sin(2*math.pi*320*t) * 0.5 + math.sin(2*math.pi*540*t) * 0.35
            + math.sin(2*math.pi*870*t) * 0.15)
    noise = random.uniform(-1, 1) * 0.3 * math.exp(-t / 0.006)
    s.append((tone + noise) * env(i, n, 0.0008, 0.035))
write("impact_knock.wav", s)

# 3) clack — กระทบแข็ง (นอยส์กรองสูง สั้นมาก)
n = int(SR * 0.12); s = []
prev = 0.0
for i in range(n):
    t = i / SR
    x = random.uniform(-1, 1)
    hp = x - prev; prev = x                       # high-pass หยาบ ๆ → เสียงแหลม
    tone = math.sin(2*math.pi*1100*t) * 0.25
    s.append((hp * 0.8 + tone) * env(i, n, 0.0005, 0.018))
write("impact_clack.wav", s)

print("\nเสร็จ — วางไฟล์เสียงของตัวเองเพิ่ม/แทนที่ในโฟลเดอร์", OUT, "ได้เลย")
