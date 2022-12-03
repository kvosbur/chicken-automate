from . import TransformationHelper
import os
import cv2

working_dir = "Transformations/ScratchDirectory"


def do_add_border(experiment_image, border_size=20):
    color = [0, 0, 0]
    image = experiment_image.get_cv2_image()
    new_image = cv2.copyMakeBorder(image, border_size, border_size, border_size, border_size, cv2.BORDER_CONSTANT, value=color)

    # file_name = os.path.join(working_dir, TransformationHelper.generate_random_image_file_name())
    # cv2.imwrite(file_name, new_image)
    experiment_image.update_cv2_image(new_image)
    # return file_name