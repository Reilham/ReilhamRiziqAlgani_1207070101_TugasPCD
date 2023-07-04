import cv2
import numpy as np
from pynput.keyboard import Controller

keyboard = Controller()

# Fungsi untuk mengontrol volume berdasarkan posisi tangan


def set_volume(position):
    # Menggunakan posisi tangan untuk mengatur volume dalam kisaran 0-100
    volume = int((position / 480) * 100)
    # Mengendalikan volume dengan menggunakan fungsi volume_down() dan volume_up()
    if volume < 50:
        for _ in range(50 - volume):
            keyboard.volume_down()
    else:
        for _ in range(volume - 50):
            keyboard.volume_up()


# Menginisialisasi webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Mengambil tinggi dan lebar frame
    height, width, _ = frame.shape

    # Mengubah frame menjadi gambar abu-abu
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Menggunakan Gaussian Blur pada gambar untuk mengurangi noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Membuat threshold pada gambar untuk menghasilkan gambar biner
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    # Menemukan kontur tangan dalam gambar biner
    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        # Mengambil kontur dengan area terbesar
        max_contour = max(contours, key=cv2.contourArea)

        # Menghitung momen kontur untuk menemukan pusat tangan
        M = cv2.moments(max_contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            # Menampilkan lingkaran di pusat tangan
            cv2.circle(frame, (cX, cY), 7, (255, 0, 0), -1)

            # Menampilkan posisi tangan pada layar
            cv2.putText(
                frame, f"Position: {cY}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Mengontrol volume berdasarkan posisi tangan
            set_volume(cY)

    # Menampilkan frame
    cv2.imshow("Volume Control", frame)

    # Menghentikan program ketika tombol 'q' ditekan
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Melepaskan sumber daya
cap.release()
cv2.destroyAllWindows()
