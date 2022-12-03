from Transformations.TransformationImage import TransformationImage
import pprint

accepted_diff = 5
def close_enough(value, target):
    global accepted_diff
    return value >= target - accepted_diff and value <= target + accepted_diff 

def pixel_same(pixel, target):
    return close_enough(pixel[0], target[0]) and close_enough(pixel[1], target[1]) and close_enough(pixel[2], target[2])

def get_longest_x_of_color(image: TransformationImage):
    p = image.get_pil_image()
    width, height = p.size
    pixels = p.load()
    start_x = 0
    longest_y = 0
    found_at_max = []
    longest_length = 0
    
    for y in range(230, 330):
        current_longth = 0
        found_green_at = -1
        for x in range(500, 650):
            pix = pixels[x, y]
            if close_enough(pix[0], 25) and close_enough(pix[1], 172) and close_enough(pix[2], 3):
                # pixel is green
                if found_green_at == -1:
                    found_green_at = x
                current_longth += 1
        print(current_longth)
        if current_longth > longest_length:
            print(current_longth, longest_length)
            longest_length = current_longth
            start_x = found_green_at
            longest_y = y
            found_at_max = [(y, found_green_at)]
        elif current_longth == longest_length:
            found_at_max.append((y, found_green_at))

    pprint.pprint(found_at_max)
    print(longest_y)
    print(start_x)
    print(longest_length)

    print((start_x - 10, longest_y - 5, start_x + longest_length + 10, longest_y + 5))

    cropped = p.crop((start_x - 10, longest_y - 5, start_x + longest_length + 10, longest_y + 5))
    print(p.getpixel((555, 273)))
    cropped.show()

def search_image(image: TransformationImage):
    p = image.get_pil_image()
    width, height = p.size
    pixels = p.load()
    
    # for y in range(230, 330):
    #     current_longth = 0
    #     found_green_at = -1
    #     for x in range(500, 650):
    #         pix = pixels[x, y]
    #         print(pix)

    print(p.size)
    cropped = p.crop((60, 2150, 1000, 2350))
    # print(p.getpixel((555, 273)))
    cropped.show()