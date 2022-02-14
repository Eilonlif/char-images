from math import gcd

import numpy as np
from PIL import Image
import sys


class image:
    def __init__(self, image, x1: int, y1: int, step: int = None, x0: int = 0, y0: int = 0, chars=None):
        im = np.array(image, dtype="uint8")
        self.height = y1 - y0
        self.width = x1 - x0
        self.step = step
        if chars is None:
            self.chars = [".", ",", "\"", "*", ";", "&", "#", "@"]
        if step is None:
            self.step = gcd(self.height, self.width)
        if not self.check_image(len(im), len(im[0])):
            raise ValueError(
                f"Something is wrong, please re-enter values\nDimensions are: {len(im[0])}x{len(im)}, step={self.step}")
        self.image = im[y0: y1, x0: x1]

    def __str__(self):
        return '\n'.join(' '.join(l) for l in self.image.tolist())

    def check_image(self, pich: int, picw: int):
        return picw >= self.width > 0 and pich >= self.height > 0 and self.height % self.step == 0 == self.width % self.step

    def gray_scale(self):
        return np.apply_along_axis(lambda x: np.dot(np.array([0.2989, 0.5870, 0.1140]), np.array(x[:3])), 2, self.image)

    def chunks(self):
        def avg(x, i, j, s):
            return np.average(x[i: i + s, j: j + s])

        ret = [([avg(self.image, i, j, self.step) for j in range(0, self.width, self.step)]) for i in
               range(0, self.height, self.step)]
        return np.array(ret)

    def generate_image(self):
        def to_chr_help(x, chars, len_chars):
            return np.array([chars[int(a / 255.0 * len_chars)] for a in x])

        return np.apply_along_axis(lambda x: to_chr_help(x, self.chars, len(self.chars)), 0, np.array(self.image))

    def write_to_file(self, file_name: str):
        with open(f"{file_name}.txt", 'w') as f:
            for i in range(self.height):
                for j in range(self.width):
                    f.write(f"{self.image[i][j]} ")
                f.write("\n")

    def show(self):
        Image.fromarray(self.image).show()

    def convert(self):
        self.image = self.gray_scale()
        self.image = self.chunks()
        self.image = self.generate_image()


def user_input(im):
    user_in = ''
    option_dictionary = dict([("print", "print the image"), ("write", "write image to a file"), ("exit", "exit"),
                              ("error", "Did not match anything, enter again!")])
    while user_in != "exit":
        for i, k_v in enumerate(list(option_dictionary.items())[:-1]):
            print(f"{i}) {k_v[0]}: {k_v[1]}")
        user_in = input("Enter an option: ")
        if user_input == "print":
            print(im)
        elif user_in == "write":
            file_name = input("Enter file name")
            print(f"Writing image to file: {file_name}")
            im.write_to_file(file_name)
        elif user_in == "exit":
            print("Exiting")
            quit()
        else:
            print(option_dictionary["error"])


def user_input_handler_no_args():
    input_list = ["x1", "y1", "step", "x0", "y0"]
    values_list = []
    for inp in input_list:
        values_list.append(int(input(f"Enter value for {inp}: ")))
    return values_list


def open_image(file_name, args):
    im = None
    try:
        with Image.open(file_name) as ima:
            im = image(ima, *args)
        im.convert()
    except FileNotFoundError:
        print("File Not Found!")
    return im


def main():
    args = sys.argv
    if len(args) == 1:
        raise ValueError("Enter a file name!")
    elif len(args) == 2:
        im = open_image(args[1], user_input_handler_no_args())
    else:
        im = open_image(args[1], list(map(int, args[2:])))
    if im is None:
        raise ValueError("Something is wrong!")
    user_input(im)


if __name__ == "__main__":
    main()
