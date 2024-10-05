from ultralytics import YOLO

model = YOLO("last.pt")

model("test.jpg")[0].show()