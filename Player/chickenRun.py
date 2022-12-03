from Transformations.TransformationImage import TransformationImage
import pprint
from .util import pixel_same, search_image
from appiumService import AppiumService


# target area is x: 509 - 601 y: 277

# the green (28, 173, 3, 255)
# the grey of empty (205, 205, 205, 255)
green_pixel = (25, 172, 0)
grey_pixel = (204, 204, 204)
toggle_on = False

def get_hatchery_percentage(image: TransformationImage):
    y = 277
    begin_x = 509
    end_x = 599
    p = image.get_pil_image()
    pixels = p.load()

    for x in range(end_x, begin_x, -1):
        if not pixel_same(pixels[x, y], grey_pixel):
            return (x - begin_x) / (end_x - begin_x)

    return 0


# location of chicken run button (60, 2150, 1000, 2350) (when it is full width)

def do_action(image: TransformationImage, appium_service: AppiumService):
    global toggle_on
    hatch_perc = get_hatchery_percentage(image)
    print("Hatch %:", hatch_perc, toggle_on)
    button_coords = (500, 2140)
    if hatch_perc > .65:
        if not toggle_on:
            toggle_on = True
            appium_service.long_press_at_coords(button_coords[0], button_coords[1], 1)
    elif hatch_perc < 0.15:
        toggle_on = False
        appium_service.tap_at_coords(500, 2000, 1)

    # for i in range (0, 2160, 50):
    #     print(i)
    #     appium_service.long_press_at_coords(50, i, 2000)
