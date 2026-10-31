# Face Detector

Also available in Chinese. Click [HERE](/README.md) to view the Chinese version of the README.

## Introduction

![License](https://img.shields.io/badge/License-MIT-dark_green)

This is a part of the [FaceDetector App](https://github.com/Zhoucheng133/FaceDetector-App), but you can also use it on its own.

## Standalone Usage

This repository can run independently of the [FaceDetector App](https://github.com/Zhoucheng133/FaceDetector-App) and supports two functions:

- `count`: Count the number of faces in images
- `draw`: Draw face boxes and confidence scores on images

### Environment Setup

```bash
# Create and activate a virtual environment (optional)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### Prepare the Model

You need a MediaPipe face detection model (`.tflite`). The repository already includes `blaze_face_full_range.tflite`, or you can download other models from the [official MediaPipe documentation](https://developers.google.com/edge/mediapipe/solutions/vision/face_detector).

### Command Syntax

```bash
python app.py <function> <input...> -m <model> [options]
```

| Argument | Required | Default | Description |
| --- | --- | --- | --- |
| `function` | Yes | - | Function to run, either `count` or `draw` |
| `input` | Yes | - | One or more image paths, separated by spaces |
| `-m, --model` | Yes | - | Path to the model file |
| `-c, --confidence` | No | `0.5` | Minimum detection confidence; lower values detect more faces |
| `-o, --output` | No | Directory of the input image | Output directory (only for `draw`) |
| `-t, --thickness` | No | `5` | Thickness of the face box (only for `draw`) |

### Counting Faces

```bash
python app.py count ./images/1.jpg ./images/2.jpg -m blaze_face_full_range.tflite
```

You can pass multiple images at once, or use a wildcard:

```bash
python app.py count ./images/*.jpg -m blaze_face_full_range.tflite
```

### Drawing Face Boxes

```bash
python app.py draw ./images/1.jpg -m blaze_face_full_range.tflite -o ./output
```

The annotated image is saved as `<original_name>_draw<original_extension>`, for example `1_draw.jpg`. If `-o` is not specified, it is saved in the same directory as the original image.

You can also adjust the confidence and line thickness:

```bash
python app.py draw ./images/1.jpg -m blaze_face_full_range.tflite -o ./output -c 0.3 -t 2
```

### Output Format

After a successful start, the program outputs an initialization message:

```json
{"ok": true, "data": "Initialized"}
```

Then it outputs one line of JSON per processed image:

```json
{"file": "./images/1.jpg", "ok": true, "data": 2}
```

For `count`, `data` is the number of faces; for `draw`, `data` is the number of faces drawn. If processing fails, `ok` is `false` and `data` contains the error message.

## Build

To run it standalone, see [Standalone Usage](#standalone-usage).

To build a binary for the [FaceDetector App](https://github.com/Zhoucheng133/FaceDetector-App), use the following commands:

```bash
# Make sure the virtual environment is activated first
pip install -r requirements.txt
pyinstaller app.spec
```

The built binary is located in `./dist`.
