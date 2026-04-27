import cv2

# Load video file
video_path = 'data/PET.mp4'  # Adjust the path to your video
cap = cv2.VideoCapture(video_path)

roi_coordinates = []  # To store the top-left and bottom-right points

def select_roi(event, x, y, flags, param):
    global roi_coordinates
    if event == cv2.EVENT_LBUTTONDOWN:
        # Record the top-left corner
        roi_coordinates = [(x, y)]
    elif event == cv2.EVENT_LBUTTONUP:
        # Record the bottom-right corner
        roi_coordinates.append((x, y))
        print(f"ROI Selected: Top-Left: {roi_coordinates[0]}, Bottom-Right: {roi_coordinates[1]}")

cv2.namedWindow("Video")
cv2.setMouseCallback("Video", select_roi)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Draw the ROI if both points are selected
    if len(roi_coordinates) == 2:
        cv2.rectangle(frame, roi_coordinates[0], roi_coordinates[1], (0, 255, 0), 2)

    cv2.imshow("Video", frame)

    # Press 'q' to exit
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Calculate ROI dimensions
if len(roi_coordinates) == 2:
    x1, y1 = roi_coordinates[0]
    x2, y2 = roi_coordinates[1]
    roi_x, roi_y = x1, y1
    roi_w, roi_h = x2 - x1, y2 - y1
    print(f"ROI Dimensions: x={roi_x}, y={roi_y}, width={roi_w}, height={roi_h}")