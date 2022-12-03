from PIL import Image
from . import TransformationHelper
import os
import cv2
import time
import numpy as np

working_dir = "Transformations/ScratchDirectory"

def do_custom_invert(image_path, threshold):
    image = Image.open(image_path)
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            pix = image.getpixel((x, y))
            if pix[0] < threshold and pix[1] < threshold and pix[2] < threshold:
                image.putpixel((x, y), (0, 0, 0))

    file_name = os.path.join(working_dir, TransformationHelper.generate_random_image_file_name())
    image.save(file_name)
    return file_name


def do_custom_invert_improv(experiment_image, threshold):

    bit_array = experiment_image.get_cv2_image()
    length_x, length_y, _ = bit_array.shape

    black_array = np.full((length_x, length_y, 3), [0,0,0], dtype=bit_array.dtype)

    cond1 = np.logical_and(bit_array[:,:,0] < threshold, bit_array[:,:,1] < threshold)
    cond2 = np.logical_and(cond1, bit_array[:,:,2] < threshold)
    my_conditional = np.full((length_x, length_y, 3), [False, False, False])
    my_conditional[:,:,0] = cond2[:,:]
    my_conditional[:,:,1] = cond2[:,:]
    my_conditional[:,:,2] = cond2[:,:]
    new_image = np.where(my_conditional, black_array[:,:], bit_array[:,:])

    experiment_image.update_cv2_image(new_image)
    # file_name = os.path.join(working_dir, TransformationHelper.generate_random_image_file_name())
    # cv2.imwrite(file_name, sol)
    # return file_name