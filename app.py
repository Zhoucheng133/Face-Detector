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

    for img_path in arguments.input:
        if arguments.function == "draw":
            output = arguments.output
            if len(arguments.input) > 1:
                p = Path(img_path)
                if output:
                    out_dir = Path(output)
                    out_dir.mkdir(parents=True, exist_ok=True)
                    output = str(out_dir / p.name)
                else:
                    output = str(p.parent / f"{p.stem}_result{p.suffix}")
            result = draw(img_path, arguments.model, arguments.confidence, output, arguments.thickness)
        else:
            result = count(img_path, arguments.model, arguments.confidence)
        sys.stdout.write(json.dumps({"file": img_path, **result}) + "\n")
        sys.stdout.flush()
