import uuid
import os
import shutil
import tempfile

ungrouped_identifier = "0"

class FileManager:

    def __init__(self):
        self.files = { ungrouped_identifier: []}
        self.debug = False
        self._setup()

    def set_debug(self, is_debug):
        self.debug = is_debug

    def _setup(self):
        self.temp_directory = tempfile.mkdtemp()

    def generate_group_identifier(self):
        group_identifier = uuid.uuid4()
        self.files[group_identifier] = []
        return group_identifier

    def generate_file_path(self, group_identifier=ungrouped_identifier, extension=".PNG"):
        file_path = os.path.join(self.temp_directory, f"Image-{uuid.uuid4()}{extension}")
        
        self.files[group_identifier].append(file_path)
        return file_path

    def remove_files_by_group_identifier(self, group_identifier):
        files_to_delete = self.files[group_identifier]

        for file in files_to_delete:
            if os.path.isfile(file):
                if self.debug:
                    print("Removing:", file)
                os.remove(file)

        del self.files[group_identifier]

    def teardown(self):
        shutil.rmtree(self.temp_directory)

File_Manager_Instance = FileManager()