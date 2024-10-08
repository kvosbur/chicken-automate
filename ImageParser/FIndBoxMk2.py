from PIL import Image
import time

from typing import Tuple, List


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
                # (
                #         pixel[0] != allowed_color[0]
                #         or pixel[1] != allowed_color[1]
                #         or pixel[2] != allowed_color[2]
                # )
                (
                    abs(pixel[0] - allowed_color[0]) > 2
                    or abs(pixel[1] - allowed_color[1]) > 2
                    or abs(pixel[2] - allowed_color[2]) > 2
                )
            )
        bools.append(bool_row)
    return bools


def converge_boxes(boxes: List[Tuple[int, int, int, int]]):
    new_boxes = []
    for box in boxes:
        should_add = True
        for new_box in new_boxes:
            # if (box[3] == new_box[3] and (new_box[0] <= box[2] <= new_box[2] or new_box[0] <= box[0] <= new_box[2])) \
            #         or (box[2] == new_box[2] and (new_box[1] <= box[3] <= new_box[3] or new_box[1] <= box[1] <= new_box[3])):
            # same left/right
            if box[0] == new_box[0] and box[2] == new_box[2] and new_box[1] > box[3]:
                should_add = False
                break
            # same end lower right
            elif box[2] == new_box[2] and box[3] == new_box[3]:
                should_add = False
                break
            # slightly different lengths around same general area
            elif (
                abs(box[0] - new_box[0]) <= 20
                and abs(box[1] - new_box[1]) <= 20
                and abs(box[2] - new_box[2]) <= 20
                and abs(box[3] - new_box[3]) <= 20
            ):
                should_add = False
                break
        if should_add:
            new_boxes.append(box)
    return new_boxes


def find_boxes(
    pil_image: Image,
    allowed_color: Tuple[int, int, int],
    min_size_x: int,
    min_size_y: int,
    x_step: int,
    y_step: int,
    start_x: int,
    start_y: int,
    end_x: int = None,
    end_y: int = None,
    different_color_in_box: bool = True,
):
    start = time.time()
    bools = make_bools(pil_image, allowed_color)
    width, height = pil_image.size

    actual_end_x = end_x
    if actual_end_x is None:
        actual_end_x = width

    actual_end_y = end_y
    if actual_end_y is None:
        actual_end_y = height

    boxes = []
    all_boxes = []
    for x in range(start_x, actual_end_x, x_step):
        # print(
        #     x,
        #     (time.time() - start) / 60,
        #     x / width * 100,
        # )
        for y in range(start_y, actual_end_y, y_step):
            if overlaps_boxes(x, y, all_boxes):
                continue
            box = find_box(
                bools,
                actual_end_x,
                actual_end_y,
                min_size_x,
                min_size_y,
                x,
                y,
                x_step,
                y_step,
            )
            if box is not None:
                all_boxes.append(box)
                if not different_color_in_box or validate_box(box, bools):
                    boxes.append(box)
                # print("found_box", x, y, box, len(boxes))
                # if len(boxes) >= 30:
                #     return boxes
    return converge_boxes(boxes)


def find_box(
    bools: Tuple[Tuple[bool]],
    width: int,
    height: int,
    min_size_x: int,
    min_size_y: int,
    start_x: int,
    start_y: int,
    step_x: int,
    step_y: int,
):
    # move right
    for x in range(start_x, width, step_x):
        if bools[x][start_y]:
            break
        if x - start_x < min_size_x:
            continue
        # move down
        for y in range(start_y, height, step_y):
            if bools[x][y]:
                break
            if y - start_y < min_size_y:
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
