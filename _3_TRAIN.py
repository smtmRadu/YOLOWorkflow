from ultralytics import YOLO
import os

# TODO: load the images into Make sense https://www.makesense.ai and create a dataset, load the labels into this folder.
# TODO: create a config.yaml file with the following content


resume = False
resume_from = "train[X]" # train/train2/train3/etc.


if __name__ == "__main__":
    if not resume:
        model = YOLO("yolo11n.pt")
        model.train(data="config.yaml", epochs=100, batch=32, lr0= 1e-3, device="0")
        
    else:
        script_path = os.path.dirname(os.path.abspath(__file__))
        resume_path = os.path.join(script_path, "runs/detect")
        resume_path = os.path.join(resume_path, f"{resume_from}/weights/last.pt")
        model = YOLO(resume_path)
        model.train(resume=resume) 