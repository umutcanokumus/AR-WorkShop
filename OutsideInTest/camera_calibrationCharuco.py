import cv2
from cv2 import aruco
import numpy as np
import glob

# === 1. PDF'ten ve ekran ölçüsünden alınan net değerler ===
squaresX = 15 ##Yatay kare
squaresY = 11 ##Dikey Kare
squareLength = 0.0125  # 12.5 cm / 15 kare = 0.0125 m
markerLength = 0.0120  # marker = 1.2 cm = 0.0120 m


dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

charuco_board = aruco.CharucoBoard_create(
    squaresX, squaresY,
    squareLength, markerLength,
    dictionary
)

# === 2. Görüntülerden köşeleri topla ===
all_corners = []
all_ids = []
image_size = None

images = glob.glob("charuco_imgs/*.jpg")  # Kalibrasyon görüntülerin burada olmalı

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    corners, ids, _ = aruco.detectMarkers(gray, dictionary)

    if ids is not None and len(corners) > 0:
        retval, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(
            markerCorners=corners,
            markerIds=ids,
            image=gray,
            board=charuco_board
        )

        if retval > 10:
            all_corners.append(charuco_corners)
            all_ids.append(charuco_ids)

            if image_size is None:
                image_size = gray.shape[::-1]

print(f"{len(all_corners)} adet geçerli görüntü işlendi.")

# === 3. Kalibrasyon ===
ret, camera_matrix, dist_coeffs, rvecs, tvecs = aruco.calibrateCameraCharuco(
    charucoCorners=all_corners,
    charucoIds=all_ids,
    board=charuco_board,
    imageSize=image_size,
    cameraMatrix=None,
    distCoeffs=None
)

print("\n✅ KALİBRASYON TAMAMLANDI")
print("RMS Reprojection Error:", ret)
print("Camera Matrix:\n", camera_matrix)
print("Distortion Coefficients:\n", dist_coeffs)

# === 4. Kaydet ===
np.savez("charuco_calibration_data.npz",
         camera_matrix=camera_matrix,
         dist_coeffs=dist_coeffs)

print("📁 Kalibrasyon verileri kaydedildi: charuco_calibration_data.npz")
