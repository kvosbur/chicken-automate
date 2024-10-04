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
from ImageParser.Dialogs import get_visible_dialogs, get_dialog_close
from Player.Research import (
    get_researches,
    has_upgrade_green,
    could_upgrade_grey,
    check_box_color,
)
from ImageParser.Util import get_box_min_y_start


def test_boxes_on_image(ti: TransformationImage):
    im = ti.get_pil_image()

    color = (39, 110, 198)
    min_size_x = (im.size[0] * 3) // 4
    min_size_y = 100
    x_step = 4
    y_step = 4
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
    components = get_ui_component_locations()

    coords = components[UIComponents.ChickenRunButton]
    appium_service.long_press_at_coords(coords[0], coords[1], 5000)


# test_startup()

File_Manager_Instance._setup()
identifier = File_Manager_Instance.generate_group_identifier()

# take_screenshot()

ti = TransformationImage("ImageParser/test-images/research-test1.png", identifier)
# test_boxes_on_image(ti)

# find_color_by_cropping(ti)
# res = get_visible_blue_dialogs(ti)
# dialog = get_visible_dialogs(ti)
# res = get_dialog_close(ti, dialog[0], dialog[1])

# res = get_purple_visible_dialogs(ti)

# print(res)
# print(get_ui_component_locations())

# putBoxesonImageTuples(ti.get_cv2_image(), res)

# pil = ti.get_pil_image()
# pil.show()
