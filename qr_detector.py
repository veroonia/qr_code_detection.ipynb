import cv2
import numpy as np

def detect_qr(image_bgr: np.ndarray):
    """
    Detect and decode QR codes from a BGR image (OpenCV format).
    Returns:
      - annotated_bgr: image with QR polygon drawn
      - decoded_texts: list of decoded strings (may be empty)
    """
    qr = cv2.QRCodeDetector()
    annotated = image_bgr.copy()
    decoded_texts = []

    # Try multiple QR codes first
    ok, decoded_info, points, _ = qr.detectAndDecodeMulti(image_bgr)
    if ok and points is not None:
        for txt, pts in zip(decoded_info, points):
            pts = pts.astype(int)
            cv2.polylines(annotated, [pts], True, (0, 255, 0), 3)
            decoded_texts.append(txt if txt else "(Detected but not decoded)")
        return annotated, decoded_texts

    # Fallback: single QR
    txt, pts, _ = qr.detectAndDecode(image_bgr)
    if pts is not None and len(pts) > 0:
        pts = pts.astype(int)
        cv2.polylines(annotated, [pts], True, (0, 255, 0), 3)
        decoded_texts.append(txt if txt else "(Detected but not decoded)")

    return annotated, decoded_texts