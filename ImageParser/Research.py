from Transformations.TransformationImage import TransformationImage
from ImageParser.FindBoxMk2 import find_boxes
from typing import Tuple, List
from enum import Enum
from ImageParser.Colors import blue_color, has_upgrade_green, could_upgrade_grey


class ResearchStateEnum(Enum):
    CanUpgrade = "Can Upgrade"
    CouldUpgrade = "Could Upgrade"
    Finished = "Finished"


class ResearchBox:
    box: Tuple[int, int, int, int]
    upgrade_location: Tuple[int, int, int, int]
    state: ResearchStateEnum

    def __init__(
        self,
        box: Tuple[int, int, int, int],
        upgrade_location: Tuple[int, int, int, int],
        state: ResearchStateEnum,
    ) -> None:
        self.box = box
        self.upgrade_location = upgrade_location
        self.state = state


def split_boxes_if_necessary(ti: TransformationImage, boxes: Tuple[int, int, int, int]):
    im = ti.get_pil_image()
    pixels = im.load()
    new_boxes = []
    for box in boxes:
        middle_x = box[0] + (box[0] + box[2]) // 2
        start_y = box[1]
        end_y = box[3]
        find_white = False
        for y in range(start_y, end_y, 5):
            pix = pixels[middle_x, y]
            if (
                find_white
                and pix[0] == blue_color[0]
                and pix[1] == blue_color[1]
                and pix[2] == blue_color[2]
            ):
                new_boxes.append((box[0], start_y, box[2], y))
                start_y = y
                find_white = False
            if pix[0] == 255 and pix[1] == 255 and pix[2] == 255:
                find_white = True
        if box[3] - start_y > 20:
            new_boxes.append((box[0], start_y, box[2], end_y))
    return new_boxes


def get_research_boxes(ti: TransformationImage):
    im = ti.get_pil_image()

    color = blue_color
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
    return res


def check_box_color(
    ti: TransformationImage, box: Tuple[int, int, int, int], color: Tuple[int, int, int]
):
    im = ti.get_pil_image()

    min_size_x = 80
    min_size_y = 80
    x_step = 4
    y_step = 4
    start_x = box[0] + (box[0] + box[2]) // 2
    start_y = box[1]
    end_x = box[2]
    end_y = box[3]

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
    return res[-1] if len(res) > 0 else None


def get_researches(ti: TransformationImage) -> List[ResearchBox]:
    boxes = get_research_boxes(ti)
    split_boxes = split_boxes_if_necessary(ti, boxes)
    sorted(split_boxes, key=lambda box: box[1])
    categorized = []
    for box in split_boxes:
        upgrade = check_box_color(ti, box, has_upgrade_green)
        if upgrade is not None:
            categorized.append(ResearchBox(box, upgrade, ResearchStateEnum.CanUpgrade))
            continue
        could_upgrade = check_box_color(ti, box, could_upgrade_grey)
        if could_upgrade:
            categorized.append(
                ResearchBox(box, could_upgrade, ResearchStateEnum.CouldUpgrade)
            )
            continue
        categorized.append(ResearchBox(box, None, ResearchStateEnum.Finished))

    return categorized
