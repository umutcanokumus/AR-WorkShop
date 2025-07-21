import cv2
import os

# Kayıt klasörü
os.makedirs("charuco_imgs", exist_ok=True)

cap = cv2.VideoCapture(0)  # Brio genelde 0 olur ama 1/2 de olabilir

if not cap.isOpened():
    print("Kamera açılamadı!")
    exit()

img_counter = 0

print("Fotoğraf çekmek için SPACE tuşuna, çıkmak için ESC tuşuna bas")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Görüntü alınamadı.")
        break

    cv2.imshow("Charuco Görüntü", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == 27:  # ESC
        break
    elif key == 32:  # SPACE tuşu → fotoğraf çek
        filename = f"charuco_imgs/img_{img_counter:02}.jpg"
        cv2.imwrite(filename, frame)
        print(f"📸 {filename} kaydedildi.")
        img_counter += 1

cap.release()
cv2.destroyAllWindows()
  