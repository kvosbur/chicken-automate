import enum

import cv2
from matplotlib.pyplot import sca

from . import TransformationHelper
import os

working_dir = "Transformations/ScratchDirectory"


class RescaleOptions(enum.Enum):
    INTER_AREA = cv2.INTER_AREA
    INTER_CUBIC = cv2.INTER_CUBIC
    INTER_LINEAR = cv2.INTER_LINEAR


def do_rescale(experiment_image, scale_x, scale_y, scale_option: RescaleOptions):
    image = experiment_image.get_cv2_image()
    new_image = cv2.resize(image, None, fx=scale_x, fy=scale_y, interpolation=scale_option.value)

    experiment_image.update_cv2_image(new_image)
    # file_name = os.path.join(working_dir, TransformationHelper.generate_random_image_file_name())
    # cv2.imwrite(file_name, new_image)
    # return file_name
