from PIL import Image
import time

from typing import Tuple


def overlaps_boxes(x, y, boxes):
    for box in boxes:
        # has same top line
        if y == box[1] and box[0] <= x <= box[2]:
            return True
    return False


def validate_box(box: Tuple[int, int, int, int], bools: Tuple[Tuple[bool]]):
    for x in range(box[0], box[2] + 1):
        for y in range(box[1], box[3] + 1):
            if bools[x][y]:
                return True
    return False


def make_bools(pil_image: Image, allowed_color: Tuple[int, int, int]):
    bools = []
    pixels = pil_image.load()
    width, height = pil_image.size
    # pre process into bools
    for x in range(width):
        bool_row = []
        for y in range(height):
            pixel = pixels[x, y]
            bool_row.append(
                (
                        pixel[0] != allowed_color[0]
                        or pixel[1] != allowed_color[1]
                        or pixel[2] != allowed_color[2]
                )
            )
        bools.append(bool_row)
    return bools


def find_boxes(
        pil_image: Image,
        allowed_color: Tuple[int, int, int],
        min_size: int,
        x_step: int,
        y_step: int,
):
    start = time.time()
    bools = make_bools(pil_image, allowed_color)
    width, height = pil_image.size

    boxes = []
    all_boxes = []
    for x in range(0, width, x_step):
        print(
            x,
            (time.time() - start) / 60,
            x / width * 100,
        )
        for y in range(0, height, y_step):
            if overlaps_boxes(x, y, all_boxes):
                continue
            box = find_box(bools, width, height, min_size, x, y, x_step, y_step)
            if box is not None:
                all_boxes.append(box)
                if validate_box(box, bools):
                    boxes.append(box)
                # print("found_box", x, y, box, len(boxes))
                # if len(boxes) >= 30:
                #     return boxes
    return boxes


def find_box(
        bools: Tuple[Tuple[bool]],
        width: int,
        height: int,
        min_size: int,
        start_x: int,
        start_y: int,
        step_x: int,
        step_y: int,
):
    # move right
    for x in range(start_x, width, step_x):
        if bools[x][start_y]:
            break
        if x - start_x < min_size:
            continue
        # move down
        for y in range(start_y, height, step_y):
            if bools[x][y]:
                break
            if y - start_y < min_size:
                continue

            is_correct = True

            # verify bottom
            for bottom_x in range(start_x, x, step_x):
                if bools[bottom_x][y]:
                    is_correct = False
                    break
            if not is_correct:
                continue

            # verify left
            for left_y in range(start_y, y, step_y):
                if bools[start_x][left_y]:
                    is_correct = False
                    break

            if is_correct:
                return (start_x, start_y, x, y)

    return None
