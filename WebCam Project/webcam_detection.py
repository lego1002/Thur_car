import cv2
import numpy as np

# ========= 可調變數 =========
scale = 0.25
target_color = 'blue'  # 可改為 'green'、'blue'，或自訂 hsv 範圍

# ========= 顏色設定函式 =========
def get_hsv_range(color_name):
    if color_name == 'red':
        return [(np.array([0, 120, 70]), np.array([10, 255, 255])),
                (np.array([160, 120, 70]), np.array([180, 255, 255]))]
    elif color_name == 'green':
        return [(np.array([35, 100, 50]), np.array([85, 255, 255]))]
    elif color_name == 'blue':
        return [(np.array([100, 150, 50]), np.array([140, 255, 255]))]
    else:
        raise ValueError("Unsupported color: use 'red', 'green', or 'blue'")

# 開啟攝影機
cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

cv2.namedWindow("Preview", cv2.WINDOW_NORMAL)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

# 取得該顏色的 HSV 區間
color_ranges = get_hsv_range(target_color)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame. Exiting ...")
        break

    corrected = cv2.flip(frame, 1)
    downscale = cv2.resize(corrected, (0, 0), fx=scale, fy=scale)

    # ===== QR code detection =====
    data, bbox, _ = detector.detectAndDecode(downscale)
    if bbox is not None:
        for i in range(len(bbox[0])):
            pt1 = tuple(map(int, bbox[0][i]))
            pt2 = tuple(map(int, bbox[0][(i + 1) % len(bbox[0])]))
            cv2.line(downscale, pt1, pt2, (0, 255, 0), 2)

        if data:
            print(f"QR Code Data: {data}")
            cv2.putText(downscale, data, (pt1[0], pt1[1] - 10),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.6, (255, 0, 0), 2)

    # ===== Color block detection =====
    hsv = cv2.cvtColor(downscale, cv2.COLOR_BGR2HSV)
    mask = np.zeros(hsv.shape[:2], dtype=np.uint8)

    # 合併多段範圍（如紅色需兩段）
    for lower, upper in color_ranges:
        mask |= cv2.inRange(hsv, lower, upper)

    # 消除雜訊
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 2000:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(downscale, (x, y), (x + w, y + h), (0, 255, 255), 2)
            cv2.putText(downscale, f"{target_color} block", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

    # 顯示結果
    cv2.imshow("Preview", downscale)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
