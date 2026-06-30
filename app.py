import argparse
import sys
from pathlib import Path

import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision


def draw_faces(image_path: str, output_path: str, min_confidence: float = 0.5):
    img_bgr = cv2.imread(str(image_path))
    if img_bgr is None:
        print(f"无法读取图片: {image_path}")
        sys.exit(1)

    h, w = img_bgr.shape[:2]
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)

    model_path = str(Path(__file__).parent / "blaze_face_full_range.tflite")
    base_options = mp_python.BaseOptions(model_asset_path=model_path)
    options = mp_vision.FaceDetectorOptions(
        base_options=base_options,
        min_detection_confidence=min_confidence,
    )
    detector = mp_vision.FaceDetector.create_from_options(options)

    result = detector.detect(mp_image)

    for det in result.detections:
        bbox = det.bounding_box
        x, y, bw, bh = bbox.origin_x, bbox.origin_y, bbox.width, bbox.height
        cv2.rectangle(img_bgr, (x, y), (x + bw, y + bh), (0, 255, 0), 2)

        score = det.categories[0].score if det.categories else 0
        label = f"{score:.2f}"
        cv2.putText(img_bgr, label, (x, max(y - 5, 15)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imwrite(str(output_path), img_bgr)
    print(f"检测到 {len(result.detections)} 张人脸")
    print(f"结果已保存: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="MediaPipe 人脸检测 - 框出人脸并输出图片")
    parser.add_argument("input", help="输入图片路径")
    parser.add_argument("-o", "--output", default=None,
                        help="输出图片路径（默认: 在输入文件名上加 _detected 后缀）")
    parser.add_argument("--confidence", type=float, default=0.5,
                        help="检测置信度阈值，默认 0.5")
    args = parser.parse_args()

    inp = Path(args.input)
    if args.output:
        out = args.output
    else:
        out = str(inp.parent / f"{inp.stem}_detected{inp.suffix}")

    draw_faces(str(inp), out, args.confidence)


if __name__ == "__main__":
    main()
