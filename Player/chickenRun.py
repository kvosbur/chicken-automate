from Transformations.TransformationImage import TransformationImage
import pprint
from .util import pixel_same, search_image
from appiumService import AppiumService


# target area is x: 509 - 601 y: 277

# the green (28, 173, 3, 255)
# the grey of empty (205, 205, 205, 255)
green_pixel = (25, 172, 0)
grey_pixel = (204, 204, 204)
chicken_run_button_coords = (500, 2140)


class ChickenRun:
    toggled_on = False
    prev_hatchery_percent = 1.1

    @staticmethod
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

    @staticmethod
    def is_hatchery_bar_full(image: TransformationImage):
        y = 277
        begin_x = 509
        end_x = 599
        p = image.get_pil_image()
        pixels = p.load()

        for x in range(end_x, begin_x, -1):
            if not pixel_same(pixels[x, y], green_pixel):
                return False

        return True

    def toggle_on(self, appium_service: AppiumService):
        print("Toggle Chicken Run ON")
        self.toggled_on = True
        appium_service.remove_long_press_at_coords(chicken_run_button_coords[0], chicken_run_button_coords[1])
        appium_service.add_long_press_at_coords(chicken_run_button_coords[0], chicken_run_button_coords[1])

    def toggle_off(self, appium_service: AppiumService):
        print("Toggle Chicken Run OFF")
        self.toggled_on = False
        appium_service.remove_long_press_at_coords(chicken_run_button_coords[0], chicken_run_button_coords[1])
        appium_service.meaningless_tap()

    # location of chicken run button (60, 2150, 1000, 2350) (when it is full width)
    def do_action(self, image: TransformationImage, appium_service: AppiumService):
        hatch_perc = ChickenRun.get_hatchery_percentage(image)
        print("Hatch %:", hatch_perc, self.toggled_on)

        if hatch_perc == 1:
            if ChickenRun.is_hatchery_bar_full(image):
                print("toggling on with full bar")
                self.toggle_on(appium_service)
        elif hatch_perc > .75:
            if not self.toggled_on or hatch_perc >= self.prev_hatchery_percent:
                self.toggle_on(appium_service)
        elif hatch_perc < 0.15:
            self.toggle_off(appium_service)
        elif hatch_perc == 0 and self.prev_hatchery_percent == 0:
            self.toggle_off(appium_service)

        self.prev_hatchery_percent = hatch_perc
