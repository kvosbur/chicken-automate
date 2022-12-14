import time
from Transformations.Util.FileManager import File_Manager_Instance
from Transformations.TransformationImage import TransformationImage
from .chickenRun import ChickenRun
from .research import Research
import subprocess
import os
from appiumService import AppiumService
import shutil

chicken_run = ChickenRun()
research = Research()
images_identifier = ""
images_directory = os.path.join(os.path.dirname(__file__), "..", "images")


def initialize():
    global images_identifier
    # File_Manager_Instance._setup()
    images_identifier = File_Manager_Instance.generate_group_identifier()
    if os.path.isdir(images_directory):
        shutil.rmtree(images_directory)
        os.mkdir(images_directory)


def take_screenshot() -> TransformationImage:
    before = time.time()
    file_path = os.path.join(images_directory, f"{time.time()}.png")
    file = open(file_path, "w")
    process = subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout=file)
    file.close()
    print("time to get next screenshot:", time.time() - before)
    return TransformationImage(file_path, images_identifier)


def do_cycle(appium_service):
    global chicken_run
    next_image = take_screenshot()
    chicken_run.do_action(next_image, appium_service)
    research.do_action(next_image, appium_service)
    appium_service.do_actions()
    print('')


def run_player(appium_service: AppiumService):
    initialize()
    time.sleep(5)
    while True:
        do_cycle(appium_service)
        time.sleep(1)


def run_test():
    # print("wait for startup")
    # time.sleep(5)
    # initialize()
    next_image = TransformationImage(os.path.join(images_directory, "..", "research1.png"), images_identifier)
    # research = Research()
    research.do_action(next_image)
