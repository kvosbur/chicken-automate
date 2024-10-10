from appiumService import AppiumService
from ImageParser.GetUiComponents import UIComponents, get_middle_from_box
from ImageParser.Dialogs import get_visible_dialogs, get_dialog_close, Dialogs
from ImageParser.ScreenshotHelper import take_screenshot
from ImageParser.Util import get_middle_from_box
import time
from typing import Tuple, Dict

all_searchable_dialogs = set([Dialogs.GrainSilos, Dialogs.HenHousing, Dialogs.Shipping])


class DiscoveredDialog:
    def __init__(
        self,
        name: Dialogs,
        open_from_coords: Tuple[int, int],
        title_bounding_box: Tuple[int, int, int, int],
        close_coords: Tuple[int, int],
    ):
        self.name = name
        self.open_from_coords = open_from_coords
        self.title_bounding_box = title_bounding_box
        self.close_coords = close_coords


def get_egg_button_dialog_info(appium_service: AppiumService, ui_components):
    # open farm dialog
    open_coords = ui_components[UIComponents.EggButton]
    appium_service.tap_at_coords(open_coords[0], open_coords[1], 1)
    time.sleep(0.5)

    ti = take_screenshot()

    # get dialog info
    dialog = get_visible_dialogs(ti)
    close_location = get_dialog_close(ti, dialog[0], dialog[1])
    close_coord = get_middle_from_box(close_location)
    appium_service.tap_at_coords(close_coord[0], close_coord[1], 1)

    return DiscoveredDialog(dialog[0], open_coords, dialog[1], close_coord)


def discover_component_screen_locations(
    appium_service: AppiumService, ui_components
) -> Dict[Dialogs, DiscoveredDialog]:
    research_button = ui_components[UIComponents.ResearchButton]
    bottom_y = research_button[1] - 100

    ti = take_screenshot()
    im = ti.get_pil_image()
    max_x = im.size[0]

    discovered = {}
    continue_processing = True

    for y in range(bottom_y, 0, -300):
        for x in range(max_x - 150, 50, -150):
            appium_service.tap_at_coords(x, y, 1)
            time.sleep(0.4)
            ti = take_screenshot()
            dialog = get_visible_dialogs(ti)
            if dialog is not None:
                # keep track of tap location for dialog if not discovered
                if dialog[0] not in discovered:
                    # close dialog
                    close_location = get_dialog_close(ti, dialog[0], dialog[1])
                    close_coord = get_middle_from_box(close_location)
                    appium_service.tap_at_coords(close_coord[0], close_coord[1], 1)

                    discovered[dialog[0]] = DiscoveredDialog(
                        dialog[0], (x, y), dialog[1], close_coord
                    )
                else:
                    close_coords = discovered[dialog[0]].close_coords
                    appium_service.tap_at_coords(close_coords[0], close_coords[1], 1)

                time.sleep(0.4)

            continue_processing = False
            for searchable_dialog in all_searchable_dialogs:
                if searchable_dialog not in list(discovered.keys()):
                    continue_processing = True

            if not continue_processing:
                break
        if not continue_processing:
            break

    discovered[Dialogs.Farm] = get_egg_button_dialog_info(appium_service, ui_components)
    return discovered
