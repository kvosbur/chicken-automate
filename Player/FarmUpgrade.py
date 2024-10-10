from appiumService import AppiumService
from ImageParser.ScreenshotHelper import take_screenshot
from ImageParser.GetUiComponents import get_middle_from_box
from ImageParser.FIndBoxMk2 import find_boxes
from ImageParser.GetUiComponents import UIComponents
from ImageParser.Dialogs import Dialogs, get_dialog_close
from ImageParser.Util import get_box_max_y_start, get_box_min_y_start
from Transformations.TransformationImage import TransformationImage
from ImageParser.Colors import has_upgrade_green
from typing import Tuple
from .UILocations import UILocations
import time


def farm_has_upgrade_boxes(ti: TransformationImage):
    im = ti.get_pil_image()

    color = has_upgrade_green
    min_size_x = (im.width * 3) // 4
    min_size_y = 100
    x_step = 4
    y_step = 10
    start_x = 0
    start_y = im.height // 4
    end_x = im.width
    end_y = im.height

    return find_boxes(
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


def do_farm_upgrade(appium_service: AppiumService, ui_locations: UILocations):
    dialog_config = ui_locations.dialogs[Dialogs.Farm]
    open_coords = dialog_config.open_from_coords
    close_coords = dialog_config.close_coords

    # open dialog
    appium_service.tap_at_coords(open_coords[0], open_coords[1], 1)
    time.sleep(0.5)

    ti = take_screenshot()

    # get upgradeable coordinates
    tappable_coordinates = farm_has_upgrade_boxes(ti)
    if len(tappable_coordinates) > 0:
        print("Upgrading Farm")
        appium_service.multi_tap(tappable_coordinates, 0.1)

    # tap dialog close
    appium_service.tap_at_coords(close_coords[0], close_coords[1], 1)
