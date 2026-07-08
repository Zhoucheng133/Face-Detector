import os
from pathlib import Path
import numpy as np

config = Path.home() / ".face_detector_cache"
config.mkdir(exist_ok=True)

os.environ["MPLCONFIGDIR"] = str(config)

import mediapipe
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision

import cv2

def count(image_path: str, model_path: str, confidence: float):
    img_bgr = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    if img_bgr is None:
        return {"ok": False, "data": "Cannot read image"}
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    mp_image = mediapipe.Image(image_format=mediapipe.ImageFormat.SRGB, data=img_rgb)
    base_options = mp_python.BaseOptions(model_asset_path=model_path)
    options = mp_vision.FaceDetectorOptions(
        base_options=base_options,
        min_detection_confidence=confidence,
    )
    detector = mp_vision.FaceDetector.create_from_options(options)
    result = detector.detect(mp_image)
    return {"ok": True, "data": len(result.detections)}
