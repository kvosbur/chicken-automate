from enum import Enum

import pytesseract
import re
from difflib import SequenceMatcher
from Transformations.TransformationImage import TransformationImage
from Transformations.AdaptiveThreshold import do_adaptive_threshold
from Transformations.ThresholdInvert import do_threshold_invert
from Transformations.CustomInvert import do_custom_invert_improv
from Transformations.Util.FileManager import File_Manager_Instance
import os
from PIL import Image
import cv2
from ocr.constants import allUpgrades
import pprint


class TesseractOption(Enum):
    DEFAULT = 3
    SINGLE_COLUMN_VARIABLE = 4
    UNIFORM_VERTICAL = 5
    UNIFORM_BLOCK = 6
    SINGLE_LINE_TEXT = 7
    SINGLE_WORD = 8
    SINGLE_WORD_IN_CIRCLE = 9
    SINGLE_CHARACTER = 10
    SPARSE_TEXT_NO_ORDER = 11
    SPARSE_TEXT_ODS = 12
    SINGLE_RAW_LINE = 13


strings_path = "dictionary.txt"


# BEST_TESSERACT_OPTIONS = [TesseractOption.UNIFORM_BLOCK, TesseractOption.SINGLE_LINE_TEXT]

# GOOD_TESSERACT_OPTIONS = [TesseractOption.DEFAULT, TesseractOption.SINGLE_COLUMN_VARIABLE, TesseractOption.UNIFORM_BLOCK,
#                           TesseractOption.SINGLE_LINE_TEXT, TesseractOption.SPARSE_TEXT_NO_ORDER, TesseractOption.SPARSE_TEXT_ODS]

# GOOD_NUMBER_TESSERACT_OPTIONS = [TesseractOption.SINGLE_COLUMN_VARIABLE, TesseractOption.UNIFORM_BLOCK,
#                           TesseractOption.SINGLE_LINE_TEXT, TesseractOption.SINGLE_CHARACTER,
#                                  TesseractOption.SPARSE_TEXT_NO_ORDER, TesseractOption.SPARSE_TEXT_ODS]

# GOOD_OVERLAP_OPTIONS = [TesseractOption.SINGLE_COLUMN_VARIABLE, TesseractOption.UNIFORM_BLOCK,
#                           TesseractOption.SINGLE_LINE_TEXT, TesseractOption.SPARSE_TEXT_NO_ORDER, TesseractOption.SPARSE_TEXT_ODS]


def bestStringMatch(parsed_string, expected_strings):
    current = parsed_string.rstrip()
    best = expected_strings[0]
    bestValue = SequenceMatcher(None, best, current).ratio()

    for string in expected_strings:
        newRatio = SequenceMatcher(None, string, current).ratio()
        if newRatio > bestValue:
            best = string
            bestValue = newRatio

    return best, bestValue


def parseImage(imageData, tesseract_option):
    parsedText = pytesseract.image_to_string(
        imageData, config=f"--psm {tesseract_option.value}"
    )
    # parsedText = pytesseract.image_to_string(imageData, config=f'--psm {tesseract_option.value} --user-words {strings_path}')
    # parsedText = pytesseract.image_to_string(imageData, config="--psm 6")  outputbase nobatch digits
    # print(parsedText)

    return parsedText


def parseNumber(imageData, tesseract_option):
    parsedText = pytesseract.image_to_string(
        imageData, config=f"--psm {tesseract_option.value} outputbase nobatch digits"
    )

    # parsedText = pytesseract.image_to_string(imageData, lang="wow-latest", config=f"--psm {tesseract_option.value}")
    # parsedText = pytesseract.image_to_string(imageData, config=f"--psm {tesseract_option.value}")

    # print("before")
    # print(parsedText)
    # print("after")

    cost = parsedText

    return cost


def putBoxesonImage(img, boxes):
    hImg, _, _ = img.shape
    for b in boxes.splitlines():
        b = b.split(" ")
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv2.rectangle(img, (x, hImg - y), (w, hImg - h), (50, 50, 255), 1)
        cv2.putText(
            img,
            b[0],
            (x, hImg - y + 13),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (50, 205, 50),
            1,
        )

    cv2.imshow("Detected text", img)
    cv2.waitKey(0)


def putBoxesonImageTuples(img, boxes):
    hImg, _, _ = img.shape
    for x, y, x2, y2 in boxes:
        cv2.rectangle(img, (x, y), (x2, y2), (255, 0, 0), 2)
        # cv2.putText(
        #     img,
        #     str(x),
        #     (x, hImg - y + 13),
        #     cv2.FONT_HERSHEY_SIMPLEX,
        #     0.4,
        #     (50, 205, 50),
        #     1,
        # )

    # cv2.imshow("Detected text", img)
    # cv2.waitKey(0)


if __name__ == "__main__":

    File_Manager_Instance._setup()
    identifier = File_Manager_Instance.generate_group_identifier()
    image = TransformationImage("screen2.png", identifier)
    # do_threshold_invert(image, 150)
    img = image.get_cv2_image()

    res = parseImage(img, TesseractOption.UNIFORM_BLOCK)
    print(res)
    foundUpgrades = []
    for line in res.split("\n"):
        bestMatch, bestRatio = bestStringMatch(line, allUpgrades)
        if bestRatio > 0.2:
            foundUpgrades.append((bestMatch, line))

    pprint.pprint(foundUpgrades)

    # boxes = pytesseract.image_to_boxes(img, config=f'--psm {TesseractOption.UNIFORM_BLOCK.value}')
    # putBoxesonImage(img, boxes)

    File_Manager_Instance.teardown()
