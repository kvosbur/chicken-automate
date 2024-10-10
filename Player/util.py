import pprint


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
