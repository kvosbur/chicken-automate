from PIL import Image
from . import TransformationHelper
from .TransformationImage import TransformationImage
import os
import cv2

working_dir = "Transformations/ScratchDirectory"


# def do_threshold_invert(image_path, threshold):
#     image = cv2.imread(image_path)
#     _, image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY_INV)
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     file_name = os.path.join(working_dir, TransformationHelper.generate_random_image_file_name())
#     cv2.imwrite(file_name, image)
#     return file_name

def do_threshold_invert(experiment_image: TransformationImage, threshold):
    image = experiment_image.get_pil_image()
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            pix = image.getpixel((x, y))
            if pix[0] > threshold or pix[1] > threshold or pix[2] > threshold:
                image.putpixel((x, y), (0, 0, 0))
            else:
                image.putpixel((x, y), (255, 255, 255))
    # file_name = os.path.join(working_dir, TransformationHelper.generate_random_image_file_name())
    # image.save(file_name)
    # return file_name
