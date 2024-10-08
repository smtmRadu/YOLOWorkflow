# YOLOWorkflow

1. Collect dataset 
    - Set the Window Title (or -1 if capturing the entire screen)
    - [Optional] Set frequency, channels, max etc.
    - Run the script and record your gameplay or whatever.
    - Stop whenever you want, screenshots were taken and saved in /images.

2. Shuffle Images and Make Sense
    - Run this script directly to shuffle the images in /images.
    - Load the images in Make Sense and start labeling.
    - Export the annotations in YOLO format, unzip them in a folder /labels.
    - TO BE DONE: A script that creates a validation folder from the images directory.

3. Train the model
    - Configure the config.yaml file with the class names, and even the path for a validation folder
    - Configure the train args and run the script.
    - If training stops without warnings, set resume var to True with correct folder name of the train session.

4. Run the model 
    - Run this script and open the app or whatever you have on the screen. The objects will be detected with an overlay.