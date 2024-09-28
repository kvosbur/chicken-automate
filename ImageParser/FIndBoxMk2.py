from PIL import Image
import time


def overlaps_boxes(x, y, boxes):
    for box in boxes:
        if (0 <= x - box[0] <= 5 and box[1] <= y <= box[3]) or (
            y == box[1] and box[0] <= x <= box[2]
        ):
            return True
    return False


def find_boxes(
    pil_image: Image,
    allowed_color: tuple[int],
    min_size: int,
):
    start = time.time()
    pixels = pil_image.load()
    width, height = pil_image.size
    boxes = []
    for x in range(width):
        print(
            x,
            (time.time() - start) / 60,
            x / (width - min_size) * 100,
        )
        for y in range(height):
            if overlaps_boxes(x, y, boxes):
                continue
            box = find_box(pixels, width, height, allowed_color, min_size, x, y)
            if box is not None:
                boxes.append(box)
                print("found_box", x, y, box, len(boxes))
                if len(boxes) >= 19:
                    return boxes
    return boxes


def find_box(
    pixels: tuple[tuple],
    width: int,
    height: int,
    allowed_color: tuple[int],
    min_size: int,
    start_x: int,
    start_y: int,
):

    # move right
    for x in range(start_x, width):
        top_pixel = pixels[x, start_y]
        if (
            top_pixel[0] != allowed_color[0]
            or top_pixel[1] != allowed_color[1]
            or top_pixel[2] != allowed_color[2]
        ):
            break
        if x - start_x < min_size:
            continue
        # move down
        for y in range(start_y, height):
            right_pixel = pixels[x, y]
            if (
                right_pixel[0] != allowed_color[0]
                or right_pixel[1] != allowed_color[1]
                or right_pixel[2] != allowed_color[2]
            ):
                break
            if y - start_y < min_size:
                continue

            is_correct = True

            # verify bottom
            for bottom_x in range(start_x, x):
                bottom_pixel = pixels[bottom_x, y]
                if (
                    bottom_pixel[0] != allowed_color[0]
                    or bottom_pixel[1] != allowed_color[1]
                    or bottom_pixel[2] != allowed_color[2]
                ):
                    is_correct = False
                    break
            if not is_correct:
                continue

            # verify left
            for left_y in range(start_y, y):
                left_pixel = pixels[start_x, left_y]
                if (
                    left_pixel[0] != allowed_color[0]
                    or left_pixel[1] != allowed_color[1]
                    or left_pixel[2] != allowed_color[2]
                ):
                    is_correct = False
                    break

            if is_correct:
                return (start_x, start_y, x, y)

    return None
