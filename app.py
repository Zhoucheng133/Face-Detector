from insightface.app import FaceAnalysis
import cv2

app = FaceAnalysis(allowed_modules=['detection'])
app.prepare(ctx_id=0, det_size=(640, 640))

img = cv2.imread("/Users/zhoucheng/Downloads/测试/test.jpg")
faces = app.get(img)

for face in faces:
    box = face.bbox.astype(int)
    cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 5) #type: ignore

cv2.imwrite("output.jpg", img) #type: ignore