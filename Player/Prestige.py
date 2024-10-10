from appiumService import AppiumService
from ImageParser.ScreenshotHelper import take_screenshot
from ImageParser.GetUiComponents import get_middle_from_box
from ImageParser.FIndBoxMk2 import find_boxes
from ImageParser.GetUiComponents import UIComponents
from ImageParser.Dialogs import Dialogs, get_dialog_close
from ImageParser.Util import get_box_max_y_start, get_box_min_y_start
from Transformations.TransformationImage import TransformationImage
from ImageParser.Colors import purple_dialog_color
from typing import Tuple
from .UILocations import UILocations
from .FarmUpgrade import open_farm_dialog
from .ConfirmationDialog import select_yes_from_confirmation_dialog
import time


def purple_button_location(ti: TransformationImage):
    im = ti.get_pil_image()

    color = purple_dialog_color
    min_size_x = (im.width * 3) // 4
    min_size_y = 70
    x_step = 4
    y_step = 10
    start_x = 0
    start_y = im.height // 4
    end_x = im.width
    end_y = im.height

    results = find_boxes(
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

    if len(results) == 0:
        raise Exception("Could not find a purple button")

    return results


def do_prestige_upgrade(appium_service: AppiumService, ui_locations: UILocations):
    open_farm_dialog(appium_service, ui_locations)

    ti = take_screenshot()

    # get prestige button coordinates and open prestige dialog
    button_coords = purple_button_location(ti)[0]
    appium_service.tap_at_coords(button_coords[0], button_coords[1], 1)
    time.sleep(0.5)

    # get prestige action button coordinates
    ti = take_screenshot()
    action_button_coords = get_box_max_y_start(purple_button_location(ti))
    appium_service.tap_at_coords(action_button_coords[0], action_button_coords[1], 1)
    time.sleep(0.5)

    # tap yes confirmation
    select_yes_from_confirmation_dialog(appium_service)
