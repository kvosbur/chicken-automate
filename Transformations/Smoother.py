import enum

import cv2

from . import TransformationHelper
import os

working_dir = "Transformations/ScratchDirectory"


def do_smooth(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    new_image = cv2.GaussianBlur(gray, (7,7), 0)

    file_name = os.path.join(working_dir, TransformationHelper.generate_random_image_file_name())
    cv2.imwrite(file_name, new_image)
    return file_name
