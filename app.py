import argparse
import json
import sys
from pathlib import Path

from utils.draw import draw
from utils.count import count

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Face Detection")
    # Functions (required)
    # [draw] Draw the faces from the image
    # [count] Count the faces from the image
    parser.add_argument("function", help="Function to run (draw/count)")

    # Input (required)
    parser.add_argument("input", nargs="+", help="Paths to image files")

    # Model (required)
    # https://developers.google.com/edge/mediapipe/solutions/vision/face_detector
    parser.add_argument("-m", "--model", required=True, help="Path to the model file")

    # Confidence (optional)
    # Lower confidence -> more faces
    parser.add_argument("-c", "--confidence", type=float, default=0.5, help="confidence threshold")

    # Output (optional, only for draw)
    # Ouput path/file name
    parser.add_argument("-o", "--output", default="", help="Output path/directory (only for draw)")

    # Draw thickness (optional, only for draw)
    parser.add_argument("-t", "--thickness", type=int, default=5, help="Thickness of the face box")

    arguments = parser.parse_args()

    if arguments.function not in ("draw", "count"):
        print(json.dumps({"ok": False, "data": "params error"}))
        sys.exit(1)

    from mediapipe.tasks import python as mp_python
    from mediapipe.tasks.python import vision as mp_vision

    base_options = mp_python.BaseOptions(model_asset_path=arguments.model)
    options = mp_vision.FaceDetectorOptions(
        base_options=base_options,
        min_detection_confidence=arguments.confidence,
    )
    global_detector = mp_vision.FaceDetector.create_from_options(options)

    print(json.dumps({"ok": True, "data": "Initialized"}))

    for img_path in arguments.input:
        if arguments.function == "draw":
            output = arguments.output
            p = Path(img_path)
            out_dir = Path(arguments.output) if arguments.output else p.parent
            out_dir.mkdir(parents=True, exist_ok=True)
            out_file = str(out_dir / f"{p.stem}_draw{p.suffix}")

            result = draw(img_path, global_detector, out_file, arguments.thickness)
        else:
            result = count(img_path, global_detector)
            
        sys.stdout.write(json.dumps({"file": img_path, **result}) + "\n")
        sys.stdout.flush()
