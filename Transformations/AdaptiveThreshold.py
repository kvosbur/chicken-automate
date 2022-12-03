from PIL import Image
from . import TransformationHelper
import os
import cv2

working_dir = "Transformations/ScratchDirectory"


def do_adaptive_threshold(experiment_image):
    image = experiment_image.get_cv2_image()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 31, 0)

    file_name = os.path.join(working_dir, TransformationHelper.generate_random_image_file_name())
    cv2.imwrite(file_name, image)

    experiment_image.update_cv2_image(image)
    # return file_name