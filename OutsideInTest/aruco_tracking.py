import cv2                  # OpenCV: görüntü işleme için ana kütüphane
from cv2 import aruco  # ArUco marker desteği (opencv-contrib içinde gelir)
import time                 # Zaman damgası almak için
import csv                  # CSV dosyasına veri kaydetmek için


# CSV log dosyasını oluştur
csv_file = open('aruco_tracking_log.csv', mode='w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Timestamp", "MarkerID", "CenterX", "CenterY"])

# ArUco sözlüğü: 4x4 50 ID'li kareler
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) ##Gri tona çevir çünkü desenle çalışcak renkle değil

    # Marker'ları tespit et
    corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    ##Köşe kodları,id'si ve kullanılmayan bilgi aruco markerın  
    if ids is not None:
        for i, corner in enumerate(corners):
            # Her bir marker'ın merkezini bul
            c = corner[0]
            cx = int((c[0][0] + c[2][0]) / 2)
            cy = int((c[0][1] + c[2][1]) / 2)

            # Marker ID'sini al
            marker_id = int(ids[i])

            # Logla
            timestamp = time.time()
            csv_writer.writerow([timestamp, marker_id, cx, cy])

            # Görselleştir
            aruco.drawDetectedMarkers(frame, corners, ids)  # Marker'ı çerçevele
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)  # Merkezine nokta koy
            cv2.putText(frame, f"ID:{marker_id} ({cx},{cy})", (cx+10, cy),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
 

    cv2.imshow("ArUco Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
csv_file.close()
cv2.destroyAllWindows()
