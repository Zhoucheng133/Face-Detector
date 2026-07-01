import argparse
import json

from utils.draw import draw
from utils.count import count

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Face Detection")
    # Functions (required)
    # [draw] Draw the faces from the image
    # [count] Count the faces from the image
    parser.add_argument("function", help="Function to run")

    # Input (required)
    parser.add_argument("input", help="Path to the image file")

    # Model (required)
    # https://developers.google.com/edge/mediapipe/solutions/vision/face_detector
    parser.add_argument("-m", "--model", help="Path to the model file")

    # Confidence (optional)
    # Lower confidence -> more faces
    parser.add_argument("-c" ,"--confidence", type=float, default=0.5, help="confidence threshold")

    # Output (optional, only for draw)
    # Ouput path/file name
    parser.add_argument("-o", "--output", default="", help="Path to the output file")

    # Draw thickness (optional, only for draw)
    parser.add_argument("-t", "--thickness", type=int, default=5, help="Thickness of the face box")

    arguments = parser.parse_args()

    if arguments.function == None or arguments.input == None or arguments.model == None:
        print(json.dumps({"ok": False, "data": "params error"}))
        exit()

    if arguments.function == "draw":
        draw(arguments.input, arguments.model, arguments.confidence, arguments.output, arguments.thickness)
    elif arguments.function == "count":
        count(arguments.input, arguments.model, arguments.confidence)
    else:
        print(json.dumps({"ok": False, "data": "params error"}))