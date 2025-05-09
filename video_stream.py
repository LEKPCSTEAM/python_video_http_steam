
from flask import Flask, Response, render_template
import cv2
import socket
import threading
import queue
from datetime import datetime
import os

app = Flask(__name__)

port = 5000

frame_queue1 = queue.Queue(maxsize=10)
frame_queue2 = queue.Queue(maxsize=10)

VIDEO_STREAMS = {
    "video1": "http://10.1.10.100:5000/video1",
    "video2": "http://10.1.10.100:5000/video2"
}

def capture_frames(camera_index, camera_name, frame_queue):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        raise RuntimeError(f"ไม่สามารถเปิดกล้อง {camera_index} ได้")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # frame = cv2.resize(frame, (640, 480))

        if camera_name == "left":
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        elif camera_name == "right":
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        if frame_queue.full():
            frame_queue.get()

        frame_queue.put(frame_bytes)

    cap.release()


def generate_frames(frame_queue):
    while True:
        if not frame_queue.empty():
            frame_bytes = frame_queue.get()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html', streams=VIDEO_STREAMS)


@app.route('/video1')
def video_feed1():
    return Response(generate_frames(frame_queue1), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video2')
def video_feed2():
    return Response(generate_frames(frame_queue2), mimetype='multipart/x-mixed-replace; boundary=frame')

SAVE_DIR = "captured_images"
os.makedirs(SAVE_DIR, exist_ok=True)

@app.route('/capture_all', methods=['POST'])
def capture_all():
    captured = []
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    for camera_name, frame_queue in [("video1", frame_queue1), ("video2", frame_queue2)]:
        try:
            frame_bytes = frame_queue.get(timeout=1)  
            filename = f"{camera_name}_{timestamp}.jpg"
            filepath = os.path.join(SAVE_DIR, filename)
            with open(filepath, 'wb') as f:
                f.write(frame_bytes)
            captured.append(f"✅ {filename}")
        except queue.Empty:
            captured.append(f"❌ {camera_name} ไม่มี frame ภายใน timeout")

    return render_template('result.html', captured=captured)


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # เชื่อมต่อปลอมไปยัง IP ใดๆ เพื่อให้ได้ IP address ปัจจุบัน
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()

if __name__ == "__main__":
    # hostname = socket.gethostname()
    ip_address = get_local_ip()
    print("============================================")
    print(f"Stream Video 1 : http://{ip_address}:{port}/video1")
    print(f"Stream Video 2 : http://{ip_address}:{port}/video2")
    print("============================================")

    thread1 = threading.Thread(target=capture_frames, args=(0, "left", frame_queue1))
    thread2 = threading.Thread(target=capture_frames, args=(2, "right", frame_queue2))

    thread1.start()
    thread2.start()

    app.run(host='0.0.0.0', port=5000)
