from Transformations.TransformationImage import TransformationImage
from .util import pixel_same
from appiumService import AppiumService
from enum import Enum
from time import time


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

    def __init__(self, state: ResearchState, begin_y: int, end_y: int):
        self.state = state
        self.begin_y = begin_y
        self.end_y = end_y

    def get_drag_coords(self, is_top=False):
        return [move_research_x_coord, self.begin_y + 5 if is_top else self.begin_y - 5]

    def get_tap_coords(self):
        return [research_x_coord, self.begin_y + ((self.end_y - self.begin_y) // 2)]

# research boundaries left: 220  right: 1010  top: 440 bottom: 1905
# dumb x to check 870
# research button pixels: 100, 2000
research_spacer_color = (39, 111, 198)
white_pixel = (255, 255, 255)
green_pixel = (25, 172, 0)
grey_pixel = (128, 128, 128)
research_button_coords = [100, 2000]
research_x_coord = 870
move_research_x_coord = 400


class Research:
    research_shown = False
    last_checked = None
    time_between_research_sec = 60

    def __init__(self):
        self.last_checked = time()

    def get_research_sections(self, image: TransformationImage):
        items = []
        p = image.get_pil_image()
        pixels = p.load()
        begin_y = 440
        end_y = 1905
        item_start_y = begin_y
        found_grey = False
        found_green = False
        in_item = False
        for y in range(begin_y, end_y, 2):
            color = pixels[research_x_coord, y]
            if not pixel_same(color, research_spacer_color) and not in_item:
                in_item = True
                item_start_y = y
            elif in_item and pixel_same(color, research_spacer_color):
                if y - item_start_y < 140:
                    pass
                else:
                    item = ResearchItem(ResearchState.from_color_status(found_grey, found_green), item_start_y, y)
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

    def toggle_show_research(self, appium_service: AppiumService):
        self.research_shown = not self.research_shown
        appium_service.tap_at_coords(research_button_coords[0], research_button_coords[1])
        if not self.research_shown:
            self.last_checked = time()

    def should_show_research(self) -> bool:
        return not self.research_shown and time() - self.last_checked >= self.time_between_research_sec

    def do_action(self, image: TransformationImage, appium_service: AppiumService=None):
        if self.should_show_research():
            print("enter research")
            self.toggle_show_research(appium_service)
            return

        sections = self.get_research_sections(image)
        if len(sections) == 0:
            # shouldn't theoretically happen, but adding this check just in case
            self.toggle_show_research(appium_service)
            return

        # go through sections looking for the first from the top that isn't finished
        target_section = sections[-1]
        for section in sections:
            if section.state != ResearchState.finished:
                target_section = section
                break

        if target_section != sections[0]:
            # need to drag to shift all researches
            appium_service.drag_from_to(target_section.get_drag_coords(), sections[0].get_drag_coords(is_top=True))
            return

        # need to check if I have enough for any of the researches
        tapped_one = False
        for section in sections:
            if section.state == ResearchState.sufficient:
                print("tapping research item")
                coords = section.get_tap_coords()
                appium_service.tap_at_coords(coords[0], coords[1])
                tapped_one = True

        if not tapped_one:
            # need logic here to get out of research and not go into it for an amount of time
            print("exit research")
            self.toggle_show_research(appium_service)
