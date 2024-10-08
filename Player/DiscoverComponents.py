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
                # close dialog
                close_location = get_dialog_close(ti, dialog[0], dialog[1])
                close_coord = get_middle_from_box(close_location)
                appium_service.tap_at_coords(close_coord[0], close_coord[1], 1)
                time.sleep(0.4)

                # keep track of tap location for dialog if not discovered
                if dialog[0] not in discovered:
                    discovered[dialog[0]] = DiscoveredDialog(
                        dialog[0], (x, y), dialog[1], close_coord
                    )

            continue_processing = False
            for searchable_dialog in all_searchable_dialogs:
                if searchable_dialog not in list(discovered.keys()):
                    continue_processing = True

            if not continue_processing:
                break
        if not continue_processing:
            break

    return discovered
