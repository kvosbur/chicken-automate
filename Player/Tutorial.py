from appiumService import AppiumService
from .PrivacyPolicyDialogs import select_accept_from_game_private_policy
from ImageParser.GetUiComponents import (
    get_chicken_run_button,
    UIComponents,
    get_bottom_menu_buttons,
)
from ImageParser.ScreenshotHelper import take_screenshot
from ImageParser.Util import alter_coords
import time


def get_past_tutorial(appium_service: AppiumService):
    time.sleep(1)
    # dismiss game privacy agreement
    select_accept_from_game_private_policy(appium_service)
    # wait for beginning graphic to go away

    coords = None
    for i in range(20):
        time.sleep(2)
        ti = take_screenshot()
        try:
            chicken_run_coords = get_chicken_run_button(
                ti, ti.get_pil_image().size[1] // 2
            )
            coords = chicken_run_coords[UIComponents.ChickenRunButton]
            break
        except:
            print("not found, trying again")
    if coords is None:
        raise Exception("Could not find chicken run button")

    # click chicken run until other buttons visible
    for i in range(100):
        appium_service.multi_tap(
            [
                alter_coords(coords, -10, 0),
                coords,
                alter_coords(coords, 10, 0),
            ],
            1,
        )
        if i % 10 == 0:
            # check if buttons are visible
            try:
                ti = take_screenshot()
                get_bottom_menu_buttons(ti)
                time.sleep(7)  # wait for final message to disappear
                return
            except:
                print("tutorial not finished")
    raise Exception("Could not detect tutorial finish")
