from Transformations.TransformationImage import TransformationImage
from ImageParser.FindBoxMk2 import find_boxes
from ImageParser.Util import get_box_min_y_start
from ocr.tess import parseImage, TesseractOption, bestStringMatch
from enum import Enum


class Dialogs(Enum):
    Shipping = "Shipping"
    MainMenu = "Main Menu"
    HenHousing = "Hen Housing"
    GrainSilos = "Grain Silos"
    Prestige = "Prestige"
    Farm = "Farm"
    Research = "Research"


Dialog_titles = {
    Dialogs.Shipping: "SHIPPING DEPOT",
    Dialogs.MainMenu: "MAIN MENU",
    Dialogs.HenHousing: "HEN HOUSING",
    Dialogs.GrainSilos: "GRAIN SILOS",
    Dialogs.Prestige: "PRESTIGE",
    Dialogs.Farm: "FARM",
    Dialogs.Research: "COMMON",
}


def get_visible_dialogs(ti: TransformationImage):
    blue_dialogs = get_visible_blue_dialogs(ti)
    if blue_dialogs is not None and blue_dialogs[1] > 0.7:
        print("blue")
        return blue_dialogs
    blue_small_dialogs = get_visible_small_blue_dialogs(ti)
    if blue_small_dialogs is not None and blue_small_dialogs[1] > 0.7:
        print("small blue")
        return blue_small_dialogs
    purple_dialogs = get_purple_visible_dialogs(ti)
    if purple_dialogs is not None and purple_dialogs[1] > 0.7:
        print("purple")
        return purple_dialogs
    return None


def get_visible_blue_dialogs(ti: TransformationImage):
    im = ti.get_pil_image()
    color = (39, 110, 198)
    min_size_x = 2 / 3 * im.size[0]
    min_size_y = 60
    x_step = 4
    y_step = 4
    start_x = 0
    start_y = 0
    end_x = im.width
    end_y = im.height // 2

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
    )
    # print(locations)
    if len(locations) == 0:
        return None

    new_ti = TransformationImage("", ti.group_identifier)
    new_ti.pil_image = im.crop(locations[-1])
    # new_ti.pil_image.show()

    tess_im = new_ti.get_cv2_image()
    results = parseImage(tess_im, TesseractOption.DEFAULT)

    best_match = bestStringMatch(
        results.replace("\n", ""), list(Dialog_titles.values())
    )

    return best_match


def get_visible_small_blue_dialogs(ti: TransformationImage):
    im = ti.get_pil_image()
    color = (39, 110, 198)
    min_size_x = im.size[0] // 4
    min_size_y = 60
    x_step = 10
    y_step = 4
    start_x = 0
    start_y = 0
    end_x = im.width
    end_y = im.height // 2

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
    )
    # print(locations)
    if len(locations) == 0:
        return None

    chosen_location = get_box_min_y_start(locations)

    new_ti = TransformationImage("", ti.group_identifier)
    new_ti.pil_image = im.crop(chosen_location)
    # new_ti.pil_image.show()

    tess_im = new_ti.get_cv2_image()
    results = parseImage(tess_im, TesseractOption.DEFAULT)

    best_match = bestStringMatch(
        results.replace("\n", ""), list(Dialog_titles.values())
    )

    return best_match


def get_purple_visible_dialogs(ti: TransformationImage):
    im = ti.get_pil_image()
    color = (134, 0, 196)
    min_size_x = 2 / 3 * im.size[0]
    min_size_y = 60
    x_step = 4
    y_step = 4
    start_x = 0
    start_y = 0
    end_x = im.width
    end_y = im.height // 2

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
    )
    # print(locations)
    if len(locations) == 0:
        return None

    new_ti = TransformationImage("", ti.group_identifier)
    new_ti.pil_image = im.crop(locations[-1])
    # new_ti.pil_image.show()

    tess_im = new_ti.get_cv2_image()
    results = parseImage(tess_im, TesseractOption.DEFAULT)

    best_match = bestStringMatch(
        results.replace("\n", ""), list(Dialog_titles.values())
    )

    return best_match
