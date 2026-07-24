================= โฟลเดอร์ ui/ : ระบบธีมของเกม =================

ธีม 1 อัน = 1 โฟลเดอร์ในนี้ (ยกเว้น _shared) ชื่อโฟลเดอร์ = ชื่อธีมใน Settings > Theme

โครงสร้าง:
  ui/
    _shared/            <- ไอคอน/ปุ่มเริ่มต้น (dark & light ใช้ + เป็น fallback ให้ทุกธีม)
      icon/  button/  background/
    <ชื่อธีม>/           <- ธีมของคุณ (ก็อป example_theme มาแก้)
      palette.json      <- สี canvas (bg/grid/axis/text/success/warning/error) — ไม่มีก็ยืม dark
      background/        <- background.png (มี=ใช้ภาพ / ไม่มี=ผู้เล่นเลือกสีเอง)
      button/           <- เฟรมปุ่ม (+ lock/ สำหรับปุ่มล็อก)
      icon/             <- ไอคอน toolbar/control (override _shared)

ลำดับการหาไฟล์ (fallback):
  ไอคอน:  ui/<ธีม>/icon/ -> ui/_shared/icon/ -> iconpho/ (โฟลเดอร์เก่า) -> ไม่มี (ไม่ใช้ emoji)
  เฟรมปุ่ม: ui/<ธีม>/button/ -> ไม่มี = ใช้สไตล์สี default

ทำธีม "สีล้วน" ได้โดยไม่ต้องมีรูป: ใช้ปุ่ม "สร้างธีมสีใหม่" ใน Settings (เขียน palette.json ให้เอง)
dark / light = hardcode สี ไม่มีโฟลเดอร์ในนี้

ไฟล์รูปทั้งหมด ❌ ห้ามมีตัวอักษร (engine เขียน text ทับให้เอง)
