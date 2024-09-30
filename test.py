from ImageParser.FIndBoxMk2 import find_boxes as find_boxes_mk2
from Player.cycle import initialize, images_identifier, take_screenshot
from Transformations.TransformationImage import TransformationImage
from Transformations.Util.FileManager import File_Manager_Instance
from ocr.tess import putBoxesonImageTuples
from pprint import pprint
from ImageParser.GetUiComponents import get_ui_component_locations, UIComponents
from ImageParser.ScreenshotHelper import take_screenshot
from appiumService import AppiumService
import time

File_Manager_Instance._setup()
identifier = File_Manager_Instance.generate_group_identifier()
# ti = TransformationImage("ImageParser/test-image.png", identifier)
# ti = take_screenshot()
# im = ti.get_pil_image()

# cropped = im.crop((60, 2150, 1000, 2350))
# print(cropped.getpixel((800, 50)))
# ti.pil_image = cropped
# wrong = set()

# for x in range(cropped.size[0]):
#     for y in range(cropped.size[1]):
#         if cropped.getpixel((x, y)) != (240, 13, 13, 255):
#             wrong.add(cropped.getpixel((x, y)))
#             # print(cropped.getpixel((x, y)))

# print(wrong)
# cropped.show()
# exit()


# res = find_boxes_mk2(im, (255, 255, 255), im.size[0] // 2, 40, 4, 10, 0, 0)

# print(res)

# putBoxesonImageTuples(ti.get_cv2_image(), res)

# pil = ti.get_pil_image()
# pil.show()
# print(get_ui_component_locations())


def test_startup():
    appium_service = AppiumService()
    time.sleep(5)
    components = get_ui_component_locations()

    coords = components[UIComponents.ChickenRunButton]
    appium_service.long_press_at_coords(coords[0], coords[1], 5000)


test_startup()
