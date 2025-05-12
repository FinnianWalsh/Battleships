import os
from tkinter import PhotoImage

images_directory = os.path.dirname(__file__)

images = {}


def photo_image(file_name: str) -> PhotoImage:
    if file_name in images:
        return images[file_name]
    image = PhotoImage(file=os.path.join(images_directory, file_name))
    images[file_name] = image
    return image
