from PIL import Image
from . import TransformationHelper
import os
import cv2

working_dir = "Transformations/ScratchDirectory"


def do_median_blur(experiment_image, size=2):
    image = experiment_image.get_cv2_image()
    new_image = cv2.blur(image, (size,size))

    # file_name = os.path.join(working_dir, TransformationHelper.generate_random_image_file_name())
    # cv2.imwrite(file_name, new_image)
    experiment_image.update_cv2_image(new_image)
    # return file_name