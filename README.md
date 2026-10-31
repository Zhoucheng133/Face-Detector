# Face Detector

Also available in English. Click [HERE](/documents/en.md) to view the English version of the README

## 简介

![License](https://img.shields.io/badge/License-MIT-dark_green)

这是[FaceDetector App](https://github.com/Zhoucheng133/FaceDetector-App)的一部分，你也可以单独使用

## 单独使用

本仓库可以脱离 [FaceDetector App](https://github.com/Zhoucheng133/FaceDetector-App) 单独运行，支持两种功能：

- `count`：统计图片中的人脸数量
- `draw`：在图片上绘制人脸框和置信度

### 环境准备

```bash
# 创建并激活虚拟环境（可选）
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### 准备模型

需要准备 MediaPipe 的人脸检测模型（`.tflite`）。仓库中已附带 `blaze_face_full_range.tflite`，也可以从 [MediaPipe 官方文档](https://developers.google.com/edge/mediapipe/solutions/vision/face_detector) 下载其他模型。

### 命令格式

```bash
python app.py <function> <input...> -m <model> [options]
```

| 参数 | 是否必填 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `function` | 是 | - | 要执行的功能，可选 `count` 或 `draw` |
| `input` | 是 | - | 一张或多张图片路径，用空格分隔 |
| `-m, --model` | 是 | - | 模型文件路径 |
| `-c, --confidence` | 否 | `0.5` | 最小检测置信度，值越低检测到的人脸越多 |
| `-o, --output` | 否 | 图片所在目录 | 输出目录（仅 `draw` 有效） |
| `-t, --thickness` | 否 | `5` | 人脸框线宽（仅 `draw` 有效） |

### 统计人脸数量

```bash
python app.py count ./images/1.jpg ./images/2.jpg -m blaze_face_full_range.tflite
```

支持一次传入多张图片，也可以使用通配符：

```bash
python app.py count ./images/*.jpg -m blaze_face_full_range.tflite
```

### 绘制人脸框

```bash
python app.py draw ./images/1.jpg -m blaze_face_full_range.tflite -o ./output
```

绘制后的图片会保存为 `<原文件名>_draw<原扩展名>`，例如 `1_draw.jpg`。如果不指定 `-o`，则保存在原图片所在目录。

还可以调整置信度和线宽：

```bash
python app.py draw ./images/1.jpg -m blaze_face_full_range.tflite -o ./output -c 0.3 -t 2
```

### 输出格式

程序启动成功后会先输出一行初始化信息：

```json
{"ok": true, "data": "Initialized"}
```

之后每处理一张图片输出一行 JSON：

```json
{"file": "./images/1.jpg", "ok": true, "data": 2}
```

其中 `count` 的 `data` 为人脸数量，`draw` 的 `data` 为绘制的人脸数量。处理失败时 `ok` 为 `false`，`data` 为错误信息。

## 构建

如果你想要单独运行，见[单独使用](#单独使用)

若要构建为二进制文件给[FaceDetector App](https://github.com/Zhoucheng133/FaceDetector-App)使用，你可以使用这个命令构建
```bash
# 注意首先进入虚拟环境
pip install -r requirements.txt
pyinstaller app.spec
```

构建完成的二进制文件在`./dist`中