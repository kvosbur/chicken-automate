import uuid
import os
import shutil


def generate_random_image_file_name(extension=".PNG"):
    return f"Image-{uuid.uuid4()}{extension}"

def transformations_setup():
    scratch_directory = os.path.join(os.path.dirname(__file__), "ScratchDirectory")
    if not os.path.isdir(scratch_directory):
        os.mkdir(scratch_directory)

def transformations_teardown():
    scratch_directory = os.path.join(os.path.dirname(__file__), "ScratchDirectory")
    if os.path.isdir(scratch_directory):
        shutil.rmtree(scratch_directory)
        os.mkdir(scratch_directory)