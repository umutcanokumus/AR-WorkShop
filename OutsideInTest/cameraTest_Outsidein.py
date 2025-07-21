import cv2            # OpenCV: Görüntü işleme kütüphanesi
import numpy as np     # Numpy: Matris işlemleri (görüntü, maskeler için)

cap = cv2.VideoCapture(0)  # 0: varsayılan kamera

if not cap.isOpened():
    print("Kamera açılamadı")
    exit()

while True:
    ret, frame = cap.read()      # Kameradan bir kare (frame) al
    if not ret:
        print("Görüntü alınamadı")  # Eğer görüntü alınamadıysa döngüden çık
        break

    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # BGR → HSV dönüşümü (renk filtresi için daha stabil)
    lower_orange = np.array([5, 100, 100])        # Alt HSV sınırı (örnek: turuncu)
    upper_orange = np.array([20, 255, 255])       # Üst HSV sınırı

    mask = cv2.inRange(hsv, lower_orange, upper_orange)  # Bu aralıkta kalan pikselleri 1 yapar (beyaz)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # Kontur (kenar) bul
    if contours:  ##contours varsa
        largest = max(contours, key=cv2.contourArea)      # En büyük şekli al
        M = cv2.moments(largest)                          # Şeklin momentlerini al (alan, ağırlık merkezi vs)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])  # X koordinatı (moment formülü)  
            cy = int(M["m01"] / M["m00"])  # Y koordinatı
            ##m00 alan,m10 x momenti,x01 y momenti,m20 x^2 momenti, m11 xy momenti
            cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)  # Yeşil nokta koy
            cv2.putText(frame, f"Sticker: ({cx}, {cy})", (cx+10, cy),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.imshow("Sticker Tracking", frame)  # Ekrana göster
    if cv2.waitKey(1) & 0xFF == ord('q'):  # q tuşuna basılırsa çık
        break


cap.release()
cv2.destroyAllWindows()
