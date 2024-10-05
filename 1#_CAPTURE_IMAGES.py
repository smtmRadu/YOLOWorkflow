import time
import os
import win32gui, win32ui, win32con, win32api
from datetime import datetime
import argparse
import numpy as np
from PIL import Image
import ctypes
from screeninfo import get_monitors

# Captures the gameplay within a window and saves the screenshots in a "data/images".
# If window title is -1, captures the entire screen.

# Required
WINDOW_TITLE = "-1"

# Not Required
FREQUENCY = 1
CHANNELS = 3 # 3=jpg, 4=png
MAX = 2**63-1

class WindowCapture:
    def __init__(self, window_title):

        if window_title == "-1":
            self.hwnd = win32gui.GetDesktopWindow()
            user32 = ctypes.windll.user32

            m = get_monitors()[0]
            self.width, self.height = m.width, m.height
        else:
            self.hwnd = win32gui.FindWindow(None, window_title)
            if not self.hwnd:
                raise Exception(f"Window '{window_title}' not found")

            window_rect = win32gui.GetWindowRect(self.hwnd)
            self.width = window_rect[2] - window_rect[0]
            self.height = window_rect[3] - window_rect[1]

        print(f"Capturing {self.width}x{self.height}")
       
    def capture_screenshot(self):
        # Get the window device context
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()

        # Create a bitmap object
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(dcObj, self.width, self.height)

        # Select the bitmap into the compatible DC
        cDC.SelectObject(bmp)

        # BitBlt to copy the window contents into the bitmap
        cDC.BitBlt((0, 0), (self.width, self.height), dcObj, (0, 0), win32con.SRCCOPY)

        # Convert the bitmap to a numpy array
        signedIntsArray = bmp.GetBitmapBits(True)
        img = np.frombuffer(signedIntsArray, dtype='uint8')
        img.shape = (self.height, self.width, 4)
  
        # Free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(bmp.GetHandle())

        # Drop the alpha channel to get RGB
        img = img[:, :, [2, 1, 0, 3]]
        pil_img = Image.fromarray(img, mode="RGBA")

        if CHANNELS == 3:
            return pil_img.convert('RGB')
        
        return pil_img


if __name__ == "__main__":
    script_path = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--title", help="Window title", default = WINDOW_TITLE, type=str)
    parser.add_argument("-f", "--frequency", help="Number of screenshots to capture per second", default = FREQUENCY, type=float)
    parser.add_argument("-c", "--channels", help="Channels in the output image that determines the extension", default = CHANNELS, type=int)
    parser.add_argument("-m", "--max", help="Maximum number of screenshots to capture", default=MAX, type = int)    

    # set the arguments
    args = parser.parse_args()
    WINDOW_TITLE = args.title
    FREQUENCY = args.frequency
    CHANNELS = args.channels
    MAX = args.max
    args = parser.parse_args()

    try:
        wincap = WindowCapture(WINDOW_TITLE)
    except Exception as e:
        print(e)
        exit()


    output_folder_path = os.path.join(script_path, "images")
    # create new folder for the dataset
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)   
    else:   
        count = 1
        while True:
            if not os.path.exists(output_folder_path + f"_{count}"):
                output_folder_path += f"_{count}"    
                os.makedirs(output_folder_path)   
                break

            count += 1




    if CHANNELS == 3:
        save_extension = "jpg"
    else:
        save_extension = "png"

    time_to_wait = 1.0/FREQUENCY
    captures_count = 0
    time_elapsed = 0.0
    current_time = time.time()

    print("Capturing...")
    while captures_count < MAX:
        delta_time = time.time() - current_time

        time_elapsed += delta_time

        if time_elapsed >= time_to_wait:
            # do the stuff
            captures_count += 1
            # print(f"Captured {captures_count} at " + datetime.now().strftime("%H:%M:%S"))
            try:
                img = wincap.capture_screenshot()
            except Exception as e:
                print(e)
                exit()
            img.save(os.path.join(output_folder_path, f"image_{captures_count}.{save_extension}"))
           
            time_elapsed = 0.0

        
        current_time += delta_time
        