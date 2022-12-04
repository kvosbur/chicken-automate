import time
from Transformations.Util.FileManager import File_Manager_Instance
from Transformations.TransformationImage import TransformationImage
from .chickenRun import ChickenRun
from .research import Research
import subprocess
import os
from appiumService import AppiumService

last_done = {}

cycle_events = {
    "chickenRun": 0
}
chicken_run = ChickenRun()
images_identifier = ""
images_directory = os.path.join(os.path.dirname(__file__), "..", "images")


def initializeLastDone():
    global last_done
    for key in cycle_events.keys():
        last_done[key] = time.time()


def initialize():
    global images_identifier
    File_Manager_Instance._setup()
    images_identifier = File_Manager_Instance.generate_group_identifier()
    initializeLastDone()


def take_screenshot() -> TransformationImage:
    before = time.time()
    file_path = os.path.join(images_directory, f"{time.time()}.png")
    file = open(file_path, "w")
    process = subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout=file)
    file.close()
    print(time.time() - before)
    return TransformationImage(file_path, images_identifier)


def do_cycle(appium_service):
    global chicken_run
    now = time.time()
    next_image = take_screenshot()
    if now - last_done["chickenRun"] >= cycle_events["chickenRun"]:
        chicken_run.do_action(next_image, appium_service)
        last_done["chickenRun"] = now


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
    research = Research()
    research.do_action(next_image)
