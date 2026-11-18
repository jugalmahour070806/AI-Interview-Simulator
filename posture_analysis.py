
import cv2
import numpy as np

# Load face detection model
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)


def analyze_posture_image(image_bytes):
    """Detect face and check camera framing."""

    image_array = np.frombuffer(
        image_bytes,
        dtype=np.uint8
    )

    frame = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )

    if frame is None:
        return None

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    if len(faces) == 0:
        return {
            "frame": frame,
            "face_detected": False,
            "centered": False
        }

    height, width = frame.shape[:2]

    x, y, w, h = max(
        faces,
        key=lambda face: face[2] * face[3]
    )

    center_x = x + w / 2

    centered = (
        width * 0.30 <= center_x <= width * 0.70
    )

    # Draw face rectangle
    for (x, y, w, h) in faces:
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

    return {
        "frame": frame,
        "face_detected": True,
        "centered": centered
    }
