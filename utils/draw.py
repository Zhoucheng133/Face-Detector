# utils/draw.py
import os
import cv2
import numpy as np
import mediapipe

def draw(image_path: str, detector, output_path: str, thickness: int):
    img_bgr = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    if img_bgr is None:
        return {"ok": False, "data": "Cannot read image"}
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    mp_image = mediapipe.Image(image_format=mediapipe.ImageFormat.SRGB, data=img_rgb)
    
    result = detector.detect(mp_image)

    if len(result.detections) == 0:
        return {"ok": True, "data": 0}

    for det in result.detections:
        bbox = det.bounding_box
        x, y, bw, bh = bbox.origin_x, bbox.origin_y, bbox.width, bbox.height
        cv2.rectangle(img_bgr, (x, y), (x + bw, y + bh), (0, 255, 0), thickness)

        score = det.categories[0].score if det.categories else 0
        label = f"{score:.2f}"
        cv2.putText(img_bgr, label, (x, max(y - 5, 15)), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3)

    suffix = os.path.splitext(output_path)[-1]
    cv2.imencode(suffix, img_bgr)[1].tofile(output_path)
    return {"ok": True, "data": len(result.detections)}
