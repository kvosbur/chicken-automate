from appiumService import AppiumService
from ImageParser.ScreenshotHelper import take_screenshot
from ImageParser.GetUiComponents import get_middle_from_box
from ImageParser.FindBoxMk2 import find_boxes
from Transformations.TransformationImage import TransformationImage
from ImageParser.Colors import blue_color
from typing import Tuple
import time


def get_coordinates_of_max_upgradeables(ti: TransformationImage):
    im = ti.get_pil_image()
    color = blue_color
    min_size_x = 70
    min_size_y = 50
    x_step = 4
    y_step = 4
    start_x = 0
    start_y = im.height // 3
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
    return [get_middle_from_box(box) for box in res]


def do_housing_action(
    appium_service: AppiumService, coords: Tuple[int, int], close_coords
):
    # open dialog
    appium_service.tap_at_coords(coords[0], coords[1], 1)
    time.sleep(0.5)

    ti = take_screenshot()

    # get upgradeable coordinates
    tappable_coordinates = get_coordinates_of_max_upgradeables(ti)
    appium_service.multi_tap(tappable_coordinates, 0.1)

    # tap dialog close
