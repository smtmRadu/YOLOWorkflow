from ultralytics import YOLO
import os

resume = False
resume_train_name = "train"


if __name__ == "__main__":

    if not resume:
        model = YOLO("yolo11n.pt")
        model.train(data="config.yaml", epochs=100, batch=32, lr0= 1e-3, device="cpu")
        
    else:
        script_path = os.path.dirname(os.path.abspath(__file__))
        resume_path = os.path.join(script_path, "runs/detect")
        resume_path = os.path.join(resume_path, f"{resume_train_name}/weights/last.pt")
        model = YOLO(resume_path)
        model.train(resume=resume) 
    #