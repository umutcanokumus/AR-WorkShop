import cv2
from cv2 import aruco
import time
import csv
import numpy as np

# CSV dosyasını oluştur
csv_file = open('aruco_tracking_3d.csv', mode='w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Timestamp", "MarkerID", "X", "Y", "Z"])

# Kamera matrisi (örnek değerler - gerçek kalibrasyon yapılabilir)
camera_matrix = np.array([
    [800, 0, 320],
    [0, 800, 240],
    [0, 0, 1]
], dtype=np.float32)

# Distorsiyon katsayıları
dist_coeffs = np.zeros((5, 1), dtype=np.float32)

# Marker fiziksel boyutu (metre cinsinden) — örn: 200 mm → 0.2 m
marker_length = 0.2

# ArUco sözlüğü ve algılama parametreleri
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()


# Kamerayı başlat
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Kamera açılamadı!")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Görüntü alınamadı.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if ids is not None:
        # Marker 3D konumunu tahmin et
        rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, marker_length, camera_matrix, dist_coeffs)

        for i, marker_id in enumerate(ids.flatten()):
            # 3D koordinatlar (metre cinsinden)
            tx, ty, tz = tvecs[i][0]
            timestamp = time.time()

            # CSV’ye yaz
            csv_writer.writerow([timestamp, marker_id, tx, ty, tz])

            # Terminale yaz
            print(f"Marker {marker_id}: X={tx:.2f} Y={ty:.2f} Z={tz:.2f} m")

            # Görsel olarak çiz
            aruco.drawDetectedMarkers(frame, corners, ids)
            aruco.drawAxis(frame, camera_matrix, dist_coeffs, rvecs[i], tvecs[i], marker_length * 0.5)

            # Ekranda yazı
            cv2.putText(frame, f"ID:{marker_id}  Z: {tz:.2f} m", (10, 30 + 30 * i),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow("3D ArUco Pose Estimation", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
csv_file.close()
cv2.destroyAllWindows()
