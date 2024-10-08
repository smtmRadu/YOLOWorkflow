import ctypes
import tkinter as tk
from ultralytics import YOLO
from _1_CAPTURE_IMAGES import WindowCapture
from threading import Thread
import queue
from screeninfo import get_monitors

# Bring the best model from runs back here in the main directory

CUSTOM_MODEL_NAME = "best.pt"
CLASSES_MAP = ['packages', 'cloud', 'x', 'y', 'z', 'w']
COLOR_MAP = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'white']

def make_click_through(window):
    hwnd = ctypes.windll.user32.FindWindowW(None, window.winfo_name())
    extended_style = ctypes.windll.user32.GetWindowLongPtrW(hwnd, -20)
    ctypes.windll.user32.SetWindowLongPtrW(hwnd, -20, extended_style | 0x80000 | 0x20)

class DetectionOverlay:
    def __init__(self, SCREEN_DIMENSIONS: tuple):
        self.root = tk.Tk()
        self.root.title("ClickThroughWindow")
        self.root.overrideredirect(True)
        self.root.geometry(f"{SCREEN_DIMENSIONS[0]}x{SCREEN_DIMENSIONS[1]}+0+0")
        self.root.wm_attributes("-topmost", True)
        self.root.attributes('-transparentcolor', 'SystemButtonFace')

        self.canvas = tk.Canvas(self.root, bg='SystemButtonFace', highlightthickness=0, width=SCREEN_DIMENSIONS[0], height=SCREEN_DIMENSIONS[1])
        self.canvas.pack()

        make_click_through(self.root)
        
        self.shape_ids = []  # Store the IDs of drawn shapes (rectangles and texts)
        self.frame_queue = queue.Queue(maxsize=1)  # Queue to hold frames for processing

    def update_detections(self, detections):
        # Remove all previous shapes
        for shape_id in self.shape_ids:
            self.canvas.delete(shape_id)
        self.shape_ids.clear()

        # Draw new rectangles and texts, and store their IDs
        for d in detections:
            x, y, width, height, color, class_name = d
            rect_id = self.canvas.create_rectangle(x, y, x + width, y + height, outline=color, width=5)
            text_id = self.canvas.create_text(x, y - 10, text=class_name, fill=color, anchor='sw', font=('Arial', 12, 'bold'))
            self.shape_ids.extend([rect_id, text_id])
        
        self.root.update()

    def capture_frames(self, cap):
        while True:
            frame = cap.capture_screenshot()
            if not self.frame_queue.full():
                self.frame_queue.put(frame)

    def process_frames(self, model):
        while True:
            if not self.frame_queue.empty():
                frame = self.frame_queue.get()
                result = model(frame, verbose=False)

                boxes = result[0].boxes
                classes = boxes.cls.cpu().numpy()
                xyxy = boxes.xyxy.cpu().numpy()

                detections = []
                for i in range(len(classes)):
                    class_id = int(classes[i])
                    x1, y1, x2, y2 = map(int, xyxy[i])
                    width = x2 - x1
                    height = y2 - y1
                    color = COLOR_MAP[class_id % len(COLOR_MAP)]
                    class_name = CLASSES_MAP[class_id % len(classes)]
                    detections.append((x1, y1, width, height, color, class_name))

                self.update_detections(detections)

    def run(self):
        model = YOLO(CUSTOM_MODEL_NAME)
        cap = WindowCapture("-1")
        
        capture_thread = Thread(target=self.capture_frames, args=(cap,))
        process_thread = Thread(target=self.process_frames, args=(model,))

        capture_thread.start()
        process_thread.start()

        self.root.mainloop()

if __name__ == "__main__":
    m = get_monitors()[0]
    overlay = DetectionOverlay(SCREEN_DIMENSIONS=(m.width, m.height))
    overlay.run()
