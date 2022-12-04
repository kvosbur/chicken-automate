from Transformations.TransformationImage import TransformationImage
import pprint
from .util import pixel_same
from appiumService import AppiumService
from enum import Enum


class ResearchState(Enum):
    finished = 0
    insufficient = 1
    sufficient = 2

    @staticmethod
    def from_color_status(has_grey, has_green):
        if has_grey:
            return ResearchState.insufficient
        if has_green:
            return ResearchState.sufficient
        return ResearchState.finished


class ResearchItem:
    state = ResearchState.insufficient
    click_location = -1

    def __init__(self, state: ResearchState, click_location: int):
        self.state = state
        self.click_location = click_location

# research boundaries left: 220  right: 1010  top: 440 bottom: 1905
# dumb x to check 870
research_spacer_color = (39, 111, 198)
white_pixel = (255, 255, 255)
green_pixel = (25, 172, 0)
grey_pixel = (128, 128, 128)


class Research:


    def get_research_sections(self, image: TransformationImage):
        items = []
        p = image.get_pil_image()
        pixels = p.load()
        x = 870
        begin_y = 440
        end_y = 1905
        found_grey = False
        found_green = False
        in_item = False
        for y in range(begin_y, end_y, 2):
            color = pixels[x, y]
            if not pixel_same(color, research_spacer_color):
                in_item = True
            elif in_item:
                item = ResearchItem(ResearchState.from_color_status(found_grey, found_green), y - 50)
                items.append(item)
                in_item = False
                found_green = False
                found_grey = False

            if in_item:
                if pixel_same(color, green_pixel):
                    found_green = True
                if pixel_same(color, grey_pixel):
                    found_grey = True

        return items


    def do_action(self, image: TransformationImage, appium_service: AppiumService=None):
        sections = self.get_research_sections(image)
        p = image.get_pil_image()
        pixels = p.load()

        x = 870

        # for y in range(0, p.size[1], 3):
        #     print("x:", x, "y:", y, pixels[x,y])
        #
        for y in range(0, p.size[1]):
            pixels[x, y] = (0, 255, 0, 255)

        # y = 1000
        # for x in range(0, p.size[0]):
        #     pixels[x, y] = (0, 255, 0, 255)

        for section in sections:
            y = section.click_location
            print(y, section.state)
            for x in range(0, p.size[0]):
                pixels[x, y] = (0, 255, 0, 255)

        p.show()
