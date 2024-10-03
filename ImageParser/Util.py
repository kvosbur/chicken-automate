from typing import Tuple


def get_box_min_y_start(boxes: Tuple[int, int, int, int]):
    lowest_y = 100000000
    best_box = None
    for box in boxes:
        if box[1] < lowest_y:
            lowest_y = box[1]
            best_box = box
    return best_box
