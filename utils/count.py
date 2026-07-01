import json

import mediapipe
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision

import cv2

def count(image_path: str, model_path: str, confidence: float):
    img_bgr = cv2.imread(str(image_path))
    if img_bgr is None:
        print(json.dumps({"ok": False, "data": "Cannot read image"}))
        return
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    mp_image = mediapipe.Image(image_format=mediapipe.ImageFormat.SRGB, data=img_rgb)
    base_options = mp_python.BaseOptions(model_asset_path=model_path)
    options = mp_vision.FaceDetectorOptions(
        base_options=base_options,
        min_detection_confidence=confidence,
    )
    detector = mp_vision.FaceDetector.create_from_options(options)
    result = detector.detect(mp_image)
    print(json.dumps({"ok": True, "data": f"{len(result.detections)} faces detected"}))