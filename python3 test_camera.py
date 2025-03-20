import cv2

cap = cv2.VideoCapture(0)  # Try 1 or 2 if 0 doesn’t work

if not cap.isOpened():
    print("❌ Camera failed to open!")
else:
    print("✅ Camera opened successfully!")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to capture video frame")
        break
    
    cv2.imshow("Camera Test", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
