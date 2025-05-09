# 📷 Dual Camera Stream & Capture with Flask

ระบบแสดงสตรีมวิดีโอจากกล้อง 2 ตัว พร้อมปุ่มถ่ายภาพแบบฝั่งเดียวหรือพร้อมกัน รองรับการทำงานผ่านเว็บเบราว์เซอร์ และจัดเก็บรูปภาพลงโฟลเดอร์

## 🔧 Features

- 📡 แสดงภาพสดจากกล้อง 2 ตัวผ่าน Web (MJPEG Stream)
- 📸 ปุ่มถ่ายภาพแยกฝั่ง (video1 / video2) และแบบพร้อมกัน
- 💾 บันทึกไฟล์ภาพลงโฟลเดอร์ `captured_images/`
- 🌐 ใช้งานผ่านเว็บเบราว์เซอร์ รองรับ Mobile / Touchscreen
- 🎨 รองรับ TailwindCSS เพื่อให้หน้าเว็บดูสวยงามและ responsive

---

## 🎬 Demo

![Demo](docs/demo.gif)

## 📁 Project Structure
```
.
├── captured_images/ # โฟลเดอร์เก็บภาพที่ถ่าย
├── templates/
│ ├── index.html # หน้าแสดงกล้องและปุ่มกด
│ └── result.html # หน้าผลลัพธ์หลังถ่ายภาพ
├── video_stream.py # ไฟล์หลักของ Flask backend
└── [README.md](http://readme.md/)
```
---

## ▶️ How to Run

### 1. ติดตั้ง Python packages

```bash
pip install flask opencv-python
2. รันเซิร์ฟเวอร์
python video_stream.py
แนะนำให้ใช้ Python 3.9+ และทดสอบกับ Raspberry Pi หรือ PC ที่มีกล้องเชื่อมต่อ

🌐 Web Interface
เมื่อรันแล้ว จะสามารถเข้าผ่านเบราว์เซอร์ในวง LAN ได้ เช่น

<http://192.168.1.100:5000/>
บนหน้าเว็บ:
🔴 ดูวิดีโอสดจากกล้องทั้งสอง

📸 ปุ่มสำหรับ Capture ฝั่งซ้ายหรือขวา

🎯 ปุ่ม Capture พร้อมกัน (ทั้ง 2 กล้อง)

🖼 Output
ภาพจะถูกบันทึกไว้ในโฟลเดอร์ captured_images/ เช่น:

```bash
captured_images/video1_20250509_112301.jpg
captured_images/video2_20250509_112301.jpg
```
⚙️ Customize
เปลี่ยน camera index ได้ที่:

```python
thread1 = threading.Thread(target=capture_frames, args=(0, "left", frame_queue1))
thread2 = threading.Thread(target=capture_frames, args=(2, "right", frame_queue2))
ปรับขนาดภาพ, หมุนภาพ, หรือความถี่ในการ capture ได้ใน capture_frames()
```
📌 Notes
รองรับกล้อง USB หรือ CSI (เช่น Raspberry Pi Camera)

- ใช้ queue เพื่อเก็บภาพล่าสุดของแต่ละกล้อง
- MJPEG stream อาจไม่เหมาะกับสตรีมระดับสูงหรือหลายเครื่องพร้อมกัน
