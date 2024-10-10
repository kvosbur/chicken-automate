from appiumService import AppiumService
from ImageParser.ScreenshotHelper import take_screenshot
from Transformations.TransformationImage import TransformationImage
from ImageParser.Colors import affirmation_green
from ImageParser.FIndBoxMk2 import find_boxes
import time


def find_yes_button(ti: TransformationImage):
    im = ti.get_pil_image()

    color = affirmation_green
    min_size_x = 200
    min_size_y = 65
    x_step = 4
    y_step = 10
    start_x = 0
    start_y = im.height // 4
    end_x = im.width
    end_y = im.height

    res = find_boxes(
        im,
        color,
        min_size_x,
        min_size_y,
        x_step,
        y_step,
        start_x,
        start_y,
        end_x,
        end_y,
        True,
    )

    if len(res) == 0:
        raise Exception("Unable to find yes confirmation")

    return res[0]


def select_yes_from_confirmation_dialog(appium_service: AppiumService):
    ti = take_screenshot()

    # find yes button
    yes_coords = find_yes_button(ti)
    appium_service.tap_at_coords(yes_coords[0], yes_coords[1], 1)

    # long sleep for farm change
    time.sleep(5)
