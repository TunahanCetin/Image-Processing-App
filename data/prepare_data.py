"""
@file prepare_sample_data.py
@brief Automatically download and save extended sample images to data/ directory.
"""

import os
from skimage import data, io
from skimage.util import img_as_ubyte

DATA_DIR = "data"

def save_image(image, filename):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    image = img_as_ubyte(image)
    path = os.path.join(DATA_DIR, filename)
    io.imsave(path, image)
    print(f"Saved: {path}")

def prepare_samples():
    print("Preparing extended sample images...")
    save_image(data.coffee(), "coffee.jpg")
    save_image(data.camera(), "camera.jpg")
    save_image(data.horse(), "horse.jpg")
    save_image(data.coins(), "coins.jpg")
    save_image(data.astronaut(), "astronaut.jpg")
    save_image(data.chelsea(), "chelsea.jpg")
    save_image(data.moon(), "moon.jpg")
    save_image(data.page(), "page.jpg")
    save_image(data.text(), "text.jpg")
    print("All samples are ready in 'data/' folder.")

if __name__ == "__main__":
    prepare_samples()
