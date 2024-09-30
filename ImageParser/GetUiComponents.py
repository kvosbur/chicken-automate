from enum import Enum
from typing import Tuple
from .FIndBoxMk2 import find_boxes
from .ScreenshotHelper import take_screenshot
from Transformations.TransformationImage import TransformationImage


def get_middle_from_box(box: Tuple[int, int, int, int]):
    return (box[0] + ((box[2] - box[0]) // 2), box[1] + ((box[3] - box[1]) // 2))


class UIComponents(Enum):
    ResearchButton = "researchToggle"
    BoostsButton = "boostsToggle"
    ChallengesButton = "challengesToggle"
    MenuButton = "menuToggle"
    EggButton = "eggButton"
    ChickenRunButton = "chickenRunButton"


def get_bottom_menu_buttons(ti: TransformationImage):
    im = ti.get_pil_image()
    locations = find_boxes(im, (255, 255, 255), 80, 80, 2, 4, 0, (im.size[1] // 3) * 2)

    if len(locations) != 4:
        raise Exception("Did not find all menu buttons", locations)

    return {
        UIComponents.ResearchButton: get_middle_from_box(locations[0]),
        UIComponents.BoostsButton: get_middle_from_box(locations[1]),
        UIComponents.ChallengesButton: get_middle_from_box(locations[2]),
        UIComponents.MenuButton: get_middle_from_box(locations[3]),
    }


def get_chicken_run_button(ti: TransformationImage, start_y):
    im = ti.get_pil_image()
    locations = find_boxes(im, (240, 13, 13), 100, 100, 2, 10, 0, start_y)

    if len(locations) == 0:
        raise Exception("Did not find chicken run button", locations)

    return {
        UIComponents.ChickenRunButton: get_middle_from_box(locations[0]),
    }


def get_egg_button(ti: TransformationImage):
    im = ti.get_pil_image()
    locations = find_boxes(im, (255, 255, 255), im.size[0] // 2, 40, 4, 10, 0, 0)

    if len(locations) == 0:
        raise Exception("Did not find reference for egg button", locations)

    box = locations[0]
    point = (box[0] - 30, box[3])

    return {
        UIComponents.EggButton: point,
    }


def get_ui_component_locations():
    screenshot = take_screenshot()
    # get bottom buttons
    bottom_buttons = get_bottom_menu_buttons(screenshot)

    # get chicken run button
    chicken_button = get_chicken_run_button(
        screenshot, bottom_buttons[UIComponents.ResearchButton][1]
    )
    bottom_buttons.update(chicken_button)

    # get egg button
    egg_button = get_egg_button(screenshot)
    bottom_buttons.update(egg_button)
    return bottom_buttons
