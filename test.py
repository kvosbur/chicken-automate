from ImageParser.FIndBoxMk2 import find_boxes as find_boxes_mk2
from Player.cycle import initialize, images_identifier, take_screenshot
from Transformations.TransformationImage import TransformationImage
from Transformations.Util.FileManager import File_Manager_Instance
from ocr.tess import putBoxesonImageTuples
import cProfile
import pstats
from pstats import SortKey
import os
import pprofile
from pprint import pprint

File_Manager_Instance._setup()
identifier = File_Manager_Instance.generate_group_identifier()
ti = TransformationImage("ImageParser/test-image6.png", identifier)
im = ti.get_pil_image()

# take_screenshot()

# cropped = im.crop((60, 2150, 1000, 2350))
# print(cropped.getpixel((20, 20)))
# ti.pil_image = cropped

# for x in range(cropped.size[0]):
#     for y in range(cropped.size[1]):
#         if cropped.getpixel((x, y)) != (255, 255, 255, 255):
#             print(cropped.getpixel((x, y)))

# cropped.show()
# exit()

# profile_result_file = "results"
# print("Running profiler")
# cProfile.run("find_boxes_mk2(im, (255, 255, 255), 80)", profile_result_file)
# p = pstats.Stats(profile_result_file)
# p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats(40)
# os.remove(profile_result_file)

res = find_boxes_mk2(im, (255, 255, 255), 100, 2, 5)
print(len(res))
pprint(res)

putBoxesonImageTuples(ti.get_cv2_image(), res)

pil = ti.get_pil_image()
pil.show()
