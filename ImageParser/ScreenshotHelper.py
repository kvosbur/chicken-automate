from Transformations.TransformationImage import TransformationImage
from Transformations.Util.FileManager import File_Manager_Instance
import time
import subprocess

images_identifier = ""


def setup():
    global images_identifier
    File_Manager_Instance._setup()
    images_identifier = File_Manager_Instance.generate_group_identifier()


def take_screenshot() -> TransformationImage:
    global images_identifier
    if images_identifier == "":
        setup()
    before = time.time()
    file_path = f"images/{time.time()}.png"
    file = open(file_path, "w")
    process = subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout=file)
    file.close()
    print(time.time() - before)
    return TransformationImage(file_path, images_identifier)
