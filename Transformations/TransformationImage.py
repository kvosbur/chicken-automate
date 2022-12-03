import uuid
import os
import cv2
from PIL import Image
from numpy import full
from .Util import File_Manager_Instance

scratch_directory = os.path.join(os.path.dirname(__file__), "ScratchDirectory")

class TransformationImage:

    def __init__(self, image_path, group_identifier):
        self.image_path = image_path
        self.group_identifier = group_identifier
        self.intermediate_file_path = ""
        self.cv2_image = None
        self.pil_image = None

    def _save_pil_image(self):
        self.intermediate_file_path = File_Manager_Instance.generate_file_path(self.group_identifier)
        self.pil_image.save(self.intermediate_file_path)
        self.pil_image.close()
        self.pil_image = None

    def _save_cv2_image(self):
        self.intermediate_file_path = File_Manager_Instance.generate_file_path(self.group_identifier)
        cv2.imwrite(self.intermediate_file_path, self.cv2_image)
        self.cv2_image = None

    def update_cv2_image(self, new_cv2_image):
        self.cv2_image = new_cv2_image

    def get_cv2_image(self):
        if self.pil_image is not None:
            self._save_pil_image()
            self.cv2_image = cv2.imread(self.intermediate_file_path)
        elif self.cv2_image is None:
            self.cv2_image = cv2.imread(self.image_path)
        return self.cv2_image

    def get_pil_image(self):
        if self.cv2_image is not None:
            self._save_cv2_image()
            self.pil_image = Image.open(self.intermediate_file_path)
        elif self.pil_image is None:
            self.pil_image =  Image.open(self.image_path)
        return self.pil_image

    def save(self):
        full_path = File_Manager_Instance.generate_file_path(self.group_identifier)
        if self.cv2_image is not None:
            cv2.imwrite(full_path, self.cv2_image)
        elif self.pil_image is not None:
            self.pil_image.save(full_path)
        return full_path

