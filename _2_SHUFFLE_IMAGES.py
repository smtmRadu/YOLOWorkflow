import os
import random
import time

if __name__ == '__main__':
    # Set a random seed for reproducibility
    random.seed(time.time())

    images_path = os.path.dirname(os.path.abspath(__file__))

    # Search all directories whose names start with "images"
    image_dirs = [os.path.join(images_path, d) for d in os.listdir(images_path) if os.path.isdir(os.path.join(images_path, d)) and d.startswith('images')]

    for img_dir in image_dirs:
        # Get all files in the directory
        files = os.listdir(img_dir)
        
        # Shuffle the files with the set seed
        random.shuffle(files)
        
        # First, rename all files to a temporary name to avoid conflicts
        temp_names = []
        for i, file in enumerate(files):
            # Get the extension of the current file
            _, extension = os.path.splitext(file)
            temp_name = f'temp_{i}{extension}'
            os.rename(os.path.join(img_dir, file), os.path.join(img_dir, temp_name))
            temp_names.append(temp_name)
        
        # Now rename the temporary files to their final shuffled names
        for i, temp_name in enumerate(temp_names):
            _, extension = os.path.splitext(temp_name)
            new_filename = f'img_{i}{extension}'  # Preserve the original extension
            os.rename(os.path.join(img_dir, temp_name), os.path.join(img_dir, new_filename))

    print(f"Images shuffled within the following directories: {image_dirs}.")

