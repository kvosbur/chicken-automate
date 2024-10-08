from ImageParser.FindBoxMk2 import find_boxes
from Player.cycle import initialize, images_identifier, take_screenshot
from Transformations.TransformationImage import TransformationImage
from Transformations.Util.FileManager import File_Manager_Instance
from ocr.tess import putBoxesonImageTuples
from pprint import pprint
from ImageParser.GetUiComponents import (
    get_ui_component_locations,
    UIComponents,
    get_welcome_back_position_if_present,
)
from ImageParser.ScreenshotHelper import take_screenshot
from appiumService import AppiumService
import time
from ImageParser.Dialogs import get_visible_dialogs, get_dialog_close, Dialogs
from ImageParser.Research import (
    get_researches,
    has_upgrade_green,
    could_upgrade_grey,
    check_box_color,
)
from ImageParser.Util import get_box_min_y_start
from Player.Research import do_research_action as do_research_action
from Player.DiscoverComponents import discover_component_screen_locations


def test_boxes_on_image(ti: TransformationImage):
    im = ti.get_pil_image()

    color = (39, 110, 198)
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

    print(res)

    putBoxesonImageTuples(ti.get_cv2_image(), res)

    pil = ti.get_pil_image()
    pil.show()


def find_color_by_cropping(ti: TransformationImage):
    im = ti.get_pil_image()
    cropped = im.crop((850, 1400, 1000, 1500))
    print(cropped.getpixel((50, 5)))
    ti.pil_image = cropped
    counts = {}

    for x in range(cropped.size[0]):
        for y in range(cropped.size[1]):
            color = cropped.getpixel((x, y))
            if color not in counts:
                counts[color] = 0
            counts[color] += 1
            # print(cropped.getpixel((x, y)))

    for key, value in counts.items():
        if value > 20:
            print(key, value)
    cropped.show()


def test_startup():
    appium_service = AppiumService()
    time.sleep(5)
    welcome_back_accept_button = get_welcome_back_position_if_present()
    if welcome_back_accept_button != None:
        appium_service.tap_at_coords(
            welcome_back_accept_button[0], welcome_back_accept_button[1], 1
        )
        # wait for dialog to disapper
        time.sleep(2)

    temp_dialog_locs = {
        Dialogs.Shipping: (930, 1612),
        Dialogs.GrainSilos: (480, 1012),
        Dialogs.HenHousing: (630, 712),
    }
    ui_components = get_ui_component_locations()
    locs = discover_component_screen_locations(appium_service, ui_components)
    print(locs)


# test_startup()

File_Manager_Instance._setup()
identifier = File_Manager_Instance.generate_group_identifier()

# take_screenshot()

ti = TransformationImage("ImageParser/test-images/hen-housing-test.png", identifier)
test_boxes_on_image(ti)

# find_color_by_cropping(ti)
# res = get_visible_blue_dialogs(ti)
# dialog = get_visible_dialogs(ti)
# print(dialog)
# res = get_dialog_close(ti, dialog[0], dialog[1])

# res = get_purple_visible_dialogs(ti)

# print(res)
# print(get_ui_component_locations())

# putBoxesonImageTuples(ti.get_cv2_image(), [dialog[1], res])

# pil = ti.get_pil_image()
# pil.show()
