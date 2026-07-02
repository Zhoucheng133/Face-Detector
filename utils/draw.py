import json
import os
import sys
from pathlib import Path
import numpy as np

config = Path.home() / ".face_detector_cache"
config.mkdir(exist_ok=True)

os.environ["MPLCONFIGDIR"] = str(config)

import mediapipe
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision
from pathlib import Path

import cv2

def draw(image_path: str, model_path: str, confidence: float, output_path: str, thickness: int):
    img_bgr = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
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
    for det in result.detections:
        bbox = det.bounding_box
        x, y, bw, bh = bbox.origin_x, bbox.origin_y, bbox.width, bbox.height
        cv2.rectangle(img_bgr, (x, y), (x + bw, y + bh), (0, 255, 0), thickness)

        score = det.categories[0].score if det.categories else 0
        label = f"{score:.2f}"
        cv2.putText(img_bgr, label, (x, max(y - 5, 15)), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3)
    if output_path=="":
        target_path = Path(image_path).parent / "result.jpg"
        suffix = os.path.splitext(target_path)[-1]
        cv2.imencode(suffix, img_bgr)[1].tofile(target_path)
    else:
        suffix = os.path.splitext(output_path)[-1]
        cv2.imencode(suffix, img_bgr)[1].tofile(output_path)
    print(json.dumps({"ok": True, "data": len(result.detections)}))
    sys.stdout.flush()
    os._exit(0)