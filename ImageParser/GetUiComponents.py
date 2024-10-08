from enum import Enum
from typing import Tuple
from .FindBoxMk2 import find_boxes
from .ScreenshotHelper import take_screenshot
from Transformations.TransformationImage import TransformationImage
from ImageParser.Colors import affirmation_green, white, hatcher_red


def get_middle_from_box(box: Tuple[int, int, int, int]):
    return (box[0] + ((box[2] - box[0]) // 2), box[1] + ((box[3] - box[1]) // 2))


accepted_diff = 5


def close_enough(value, target):
    global accepted_diff
    return value >= target - accepted_diff and value <= target + accepted_diff


def pixel_same(pixel, target):
    return (
        close_enough(pixel[0], target[0])
        and close_enough(pixel[1], target[1])
        and close_enough(pixel[2], target[2])
    )


class UIComponents(Enum):
    ResearchButton = "researchToggle"
    BoostsButton = "boostsToggle"
    ChallengesButton = "challengesToggle"
    MenuButton = "menuToggle"
    EggButton = "eggButton"
    ChickenRunButton = "chickenRunButton"
    HatchBar = "hatchBar"


def get_welcome_back_position_if_present():
    screenshot = take_screenshot()
    im = screenshot.get_pil_image()
    color = affirmation_green
    min_size_x = 2 / 3 * im.size[0]
    min_size_y = 30
    x_step = 2
    y_step = 2
    start_x = 0
    start_y = 0

    locations = find_boxes(
        im, color, min_size_x, min_size_y, x_step, y_step, start_x, start_y
    )

    if len(locations) == 0:
        return None
    else:
        return get_middle_from_box(locations[0])


def get_hatch_bar_location(ti: TransformationImage):
    im = ti.get_pil_image()
    color = affirmation_green
    min_size_x = 40
    min_size_y = 10
    x_step = 2
    y_step = 2
    start_x = 0
    start_y = 0
    end_x = im.width
    end_y = im.height

    locations = find_boxes(
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
        False,
    )

    if len(locations) == 0:
        raise Exception("unable to find hatch bar")

    center = get_middle_from_box(locations[0])
    pixels = im.load()
    # find top
    top = center[1]
    while top > 0:
        if not pixel_same(pixels[center[0], top], color):
            top += 1
            break
        top -= 1

    # find bottom
    bottom = center[1]
    while bottom < im.height:
        if not pixel_same(pixels[center[0], top], color):
            top -= 1
            break
        top += 1

    middle = top + ((bottom - top) // 2)

    # find left
    left = center[0]
    while left > 0:
        if not pixel_same(pixels[left, middle], color):
            top += 1
            break
        left -= 1

    # find right
    right = center[0]
    while right < im.width:
        if not pixel_same(pixels[right, middle], color):
            right -= 1
            break
        right += 1

    # add 5 pixel buffer to deal with possible slight differences between screenshots
    return {UIComponents.HatchBar: (left + 5, middle, right - 5, middle)}


def get_bottom_menu_buttons(ti: TransformationImage):
    im = ti.get_pil_image()
    locations = find_boxes(
        im,
        white,
        80,
        80,
        2,
        4,
        0,
        (im.size[1] // 3) * 2,
    )

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
    locations = find_boxes(im, hatcher_red, 100, 100, 2, 10, 0, start_y)

    if len(locations) == 0:
        raise Exception("Did not find chicken run button", locations)

    return {
        UIComponents.ChickenRunButton: get_middle_from_box(locations[0]),
    }


def get_egg_button(ti: TransformationImage):
    im = ti.get_pil_image()
    locations = find_boxes(im, white, im.size[0] // 2, 40, 4, 10, 0, 0)

    if len(locations) == 0:
        raise Exception("Did not find reference for egg button", locations)

    box = locations[0]
    point = (box[0] - 30, box[3])

    return {
        UIComponents.EggButton: point,
    }


def get_ui_component_locations():
    print("get ui elements")
    screenshot = take_screenshot()
    ui_components = {}
    # get bottom buttons
    bottom_buttons = get_bottom_menu_buttons(screenshot)
    ui_components.update(bottom_buttons)

    # get chicken run button
    chicken_button = get_chicken_run_button(
        screenshot, bottom_buttons[UIComponents.ResearchButton][1]
    )
    ui_components.update(chicken_button)

    # get egg button
    egg_button = get_egg_button(screenshot)
    ui_components.update(egg_button)

    # get hatch bar
    hatch_bar = get_hatch_bar_location(screenshot)
    ui_components.update(hatch_bar)
    return ui_components
