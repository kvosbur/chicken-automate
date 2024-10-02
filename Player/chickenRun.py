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


def get_hatchery_percentage(image: TransformationImage, hatchery_location):
    y = hatchery_location[1]
    begin_x = hatchery_location[0]
    end_x = hatchery_location[2]
    p = image.get_pil_image()
    pixels = p.load()

    for x in range(end_x, begin_x, -1):
        if not pixel_same(pixels[x, y], grey_pixel):
            return (x - begin_x) / (end_x - begin_x)

    return 0


# location of chicken run button (60, 2150, 1000, 2350) (when it is full width)


def do_action(
    image: TransformationImage,
    appium_service: AppiumService,
    hatchery_location,
    chicken_run_button,
):
    global toggle_on
    hatch_perc = get_hatchery_percentage(image, hatchery_location)
    print("Hatch %:", hatch_perc, toggle_on)
    if hatch_perc > 0.65:
        if not toggle_on:
            toggle_on = True
            appium_service.long_press_at_coords(
                chicken_run_button[0], chicken_run_button[1], 1
            )
    elif hatch_perc < 0.15:
        toggle_on = False
        appium_service.long_press_at_coords(0, chicken_run_button[1], 0.2)
