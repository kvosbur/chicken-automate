from appiumService import AppiumService
from ImageParser.ScreenshotHelper import take_screenshot
from Transformations.TransformationImage import TransformationImage
from ImageParser.Colors import blue_color
from ImageParser.FIndBoxMk2 import find_boxes
from ImageParser.Util import get_middle_from_box
import time


def find_game_privacy_policy_accept_button(ti: TransformationImage):
    im = ti.get_pil_image()

    color = blue_color
    min_size_x = 120
    min_size_y = 50
    x_step = 2
    y_step = 2
    start_x = 0
    start_y = 0
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
        raise Exception("Unable to find game privacy policy accept button")
    return get_middle_from_box(res[0])


def select_accept_from_game_private_policy(appium_service: AppiumService):
    ti = take_screenshot()

    # tap accept button
    accept_coords = find_game_privacy_policy_accept_button(ti)
    appium_service.tap_at_coords(accept_coords[0], accept_coords[1], 1)
