from appiumService import AppiumService
from ImageParser.ScreenshotHelper import take_screenshot
from ImageParser.GetUiComponents import get_middle_from_box
from ImageParser.FIndBoxMk2 import find_boxes
from ImageParser.Dialogs import Dialogs
from ImageParser.Util import get_box_max_y_start, get_box_min_y_start
from Transformations.TransformationImage import TransformationImage
from ImageParser.Colors import blue_color, background_dialog_grey
from typing import Tuple
from .UILocations import UILocations
import time

down_last = False


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


def get_coordinates_of_all(ti: TransformationImage):
    im = ti.get_pil_image()
    color = background_dialog_grey
    min_size_x = (im.width * 3) // 4
    min_size_y = 70
    x_step = 4
    y_step = 4
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
    return [get_middle_from_box(box) for box in res]


def do_shipping_action(appium_service: AppiumService, ui_locations: UILocations):
    global down_last
    dialog_config = ui_locations.dialogs[Dialogs.Shipping]
    open_coords = dialog_config.open_from_coords
    close_coords = dialog_config.close_coords

    # open dialog
    appium_service.tap_at_coords(open_coords[0], open_coords[1], 1)
    time.sleep(0.5)

    swipe_count = 3
    while swipe_count >= 0:
        ti = take_screenshot()
        upgradeables = get_coordinates_of_max_upgradeables(ti)
        if len(upgradeables) > 0:
            appium_service.multi_tap(upgradeables, 0.1)
            break
        option_boxes = get_coordinates_of_all(ti)
        upper_item = get_box_min_y_start(option_boxes)  # top of screen
        lower_item = get_box_max_y_start(option_boxes)  # bottom of screen

        drag_from = lower_item
        drag_to = upper_item
        if down_last:
            drag_from = upper_item
            drag_to = lower_item
        print("drag from", drag_from, "drag to", drag_to, down_last)

        appium_service.drag(
            drag_from[0] - 300, drag_from[1], drag_to[0] - 300, drag_to[1]
        )
        swipe_count -= 1
    down_last = not down_last

    # tap dialog close
    appium_service.tap_at_coords(close_coords[0], close_coords[1], 1)
