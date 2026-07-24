========================================
 NEWTON PHYSICS SIMULATOR
========================================

[ ติดตั้ง ]
  pip install pygame-ce pygame_gui
  (requests ไม่ต้องลง — AI ใช้ urllib ที่มากับ Python อยู่แล้ว)

[ รัน ]
  python main.py

[ โครงสร้างโฟลเดอร์ที่ต้องมี ]
  PHYSICS_GAME/
  ├── main.py                ← ไฟล์รันหลัก
  ├── physics.py             ← เครื่องยนต์ฟิสิกส์ (SAT collision, CoM, spring/rope)
  ├── ui_core.py             ← UI หลัก + ปุ่ม + หน้าต่างตั้งค่า
  ├── whiteboard.py          ← กระดานวาด
  ├── config.py              ← ค่าคงที่ + ธีม + time chamber config
  ├── progress.py            ← เซฟ API key / time chamber settings
  ├── world_manager.py       ← เซฟ/โหลดโลก
  ├── missions.py            ← มิชชัน
  ├── calculator.py          ← คำนวณเวกเตอร์
  ├── graph_ui.py            ← กราฟ + เข็มทิศ telemetry
  ├── ai_assistant.py        ← เชื่อม Gemini API (urllib)
  ├── ai_ui.py               ← หน้าต่างแชท AI
  ├── time_chamber.py        ← จัดการหน่วยความจำย้อนเวลา
  ├── ui_calculator.py       ← เครื่องคิดเลขบนกระดาน
  ├── ui_drag_arrow.py       ← ลากตั้งความเร็ว
  ├── theme_kanit.json       ← ธีมฟอนต์ Kanit (ใช้เมื่อมีไฟล์ฟอนต์)
  ├── theme_noto.json        ← ธีมฟอนต์ noto_sans (สำรอง รองรับไทย)
  │
  ├── iconpho/               ← (ไม่บังคับ) ไอคอน PNG ของปุ่ม — ดู _README.txt
  ├── fonts/                 ← (ไม่บังคับ) ฟอนต์ Kanit — ดู _README.txt
  └── worlds/                ← สร้างอัตโนมัติ เก็บโลก+มิชชัน
       ├── saved_world/
       └── mission_world/

[ เรื่องฟอนต์ไทย ]
  - ถ้าไม่ทำอะไรเลย: ใช้ noto_sans (มากับ pygame_gui) → ไทยอ่านได้ ไม่เป็นกล่อง
  - ถ้าอยากสวยขึ้น: ใส่ Kanit ในโฟลเดอร์ fonts/ (ดู fonts/_README.txt)

[ เรื่อง AI (Gemini) ]
  - เข้าเมนู → ใส่ Google AI Studio API Key → SAVE
  - เลือกโมเดล Gemini ได้ (ไม่มีตัวสร้างภาพ)
  - ถ้าไม่ใส่ key ปุ่ม AI จะล็อก

[ ปุ่ม Time Chamber (ย้อนเวลา) ]
  - หน้าเมนูมีปุ่มตั้งค่า → กำหนดขนาด RAM (MB), sample rate, ring buffer → APPLY
  - ในเกม: หยุด (PAUSE) แล้วลาก slider หรือกด ⏮ ⏭ เลื่อนทีละเฟรม
  - แถบ memory มุมขวาล่างบอกว่าใช้ RAM ไปเท่าไหร่
