from PIL import Image
import os
from os import path
import PIL
import numpy as np
import multiprocessing as mp


class Resize:
    def __init__(self, image, input_path, output_path, count, fixed_height=2048):
        self.image = image
        self.input_path = input_path
        self.output_path = output_path
        self.fixed_height = fixed_height
        self.count = count
        self.main()

    def main(self):
        if (path.exists(self.output_path)):
            image = Image.open(f"{self.input_path}/{self.image}")
            height_percent = (self.fixed_height / float(image.size[1]))
            width_size = int((float(image.size[0]) * float(height_percent)))
            image = image.resize((width_size, self.fixed_height), PIL.Image.NEAREST)
            image.save(f"{self.output_path}/{self.image}")
            print(f"✔ [{self.count + 1}]{self.image}")
        else:
            os.mkdir(self.output_path)
            image = Image.open(f"{self.input_path}/{self.image}")
            height_percent = (self.fixed_height / float(image.size[1]))
            width_size = int((float(image.size[0]) * float(height_percent)))
            image = image.resize((width_size, self.fixed_height), PIL.Image.NEAREST)
            image.save(f"{self.output_path}/{self.image}")
            print(f"✔ [{self.count + 1}]{self.image}")

class FindImage:
    def __init__(self, input_path, file_ext):
        self.input_path = input_path
        self.file_ext = file_ext

    def getPaths(self):
        items = next(os.walk(self.input_path))[2]
        file_lists = []
        for item in items:
            file_ext = os.path.splitext(item)
            if file_ext[1] in self.file_ext:
                file_lists.append(item)
            else:
                continue
        return file_lists


class Main():
    def __init__(self, input_path, output_path, fixed_height, newarr):
        self.input_path = input_path
        self.output_path = output_path
        self.fixed_height = fixed_height
        self.newarr = newarr
        self.main_process()

    def main_process(self):
        for item in self.newarr:
            Resize(item, self.input_path, self.output_path, self.fixed_height)

if __name__ == '__main__':
    input_path = input("input_path : ")
    output_path = input("output_path : ")
    try:
        fixed_height = int(input("fixed_height [default = 2048] : "))
    except ValueError:
        fixed_height = 2048

    try:
        thread = int(input("thread [default = 3] : "))
    except ValueError:
        thread = 3
    paths = FindImage(input_path, [".JPG"]).getPaths()
    arr = np.array(paths)
    newarrs = np.array_split(arr, thread)

    print("**************************************")
    print(f"Size Image         : {str(fixed_height)}")
    print(f"Number of pictures : {len(paths)}")
    print(f"Thread             : {thread}")
    print("**************************************")

    pp = []
    for newarr in newarrs:
        if len(newarr) != 0:
            thr1 = Main(fixed_height=fixed_height, input_path=input_path, output_path=output_path, newarr=newarr)
            p1 = mp.Process(target=thr1.main_process())
            p1.start()
            pp.append(p1)
        else:
            continue

    for p in pp:
        p.join()
    input("finished.")
