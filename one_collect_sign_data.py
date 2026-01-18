import os
import cv2
import string
import time

# Initialize webcam
cap = cv2.VideoCapture(0)

# Directory to save images
directory = 'Image/'
os.makedirs(directory, exist_ok=True)
# Create folders for each letter if they don't exist
for letter in string.ascii_uppercase:
    os.makedirs(os.path.join(directory, letter), exist_ok=True)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break   

    # Flip the frame like a mirror
    # frame = cv2.flip(frame, 1)

    # Display rectangle for ROI
    cv2.rectangle(frame, (0, 40), (300, 400), (255, 255, 255), 2)
    cv2.putText(frame, "Press A-Z to capture 30 images", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)

    # Show video feed
    cv2.imshow("data", frame)

    # Wait for key press
    interrupt = cv2.waitKey(10)
    if interrupt & 0xFF in [ord(letter) for letter in string.ascii_lowercase]:
        key_char = chr(interrupt & 0xFF)
        folder_path = os.path.join(directory, key_char.upper())
        current_count = len(os.listdir(folder_path))

        print(f"📸 Capturing 30 images for: {key_char.upper()}")
        for i in range(30):
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                continue

            roi = frame[40:400, 0:300]
            save_path = os.path.join(folder_path, f"{current_count + i}.png")
            cv2.imwrite(save_path, roi)

            # Show progress
            cv2.putText(roi, f"{i+1}/30", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.imshow("Capturing...", roi)
            cv2.waitKey(100)  # Delay between captures

        print(f"✅ Done capturing for: {key_char.upper()}\n")

    elif interrupt & 0xFF == 27:  # Press ESC to exit
        print("Exiting...")
        break

# Release everything
cap.release()
cv2.destroyAllWindows()
