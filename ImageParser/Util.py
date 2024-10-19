from typing import Tuple


def get_box_min_y_start(boxes: Tuple[int, int, int, int]):
    lowest_y = 100000000
    best_box = None
    for box in boxes:
        if box[1] < lowest_y:
            lowest_y = box[1]
            best_box = box
    return best_box


def get_box_max_y_start(boxes: Tuple[int, int, int, int]):
    highest_y = -1
    best_box = None
    for box in boxes:
        if box[1] > highest_y:
            highest_y = box[1]
            best_box = box
    return best_box


def get_middle_from_box(box: Tuple[int, int, int, int]):
    return (box[0] + ((box[2] - box[0]) // 2), box[1] + ((box[3] - box[1]) // 2))


def alter_coords(
    coord: Tuple[int, int], x_change: int, y_change: int
) -> Tuple[int, int]:
    return (coord[0] - x_change, coord[1] - y_change)
