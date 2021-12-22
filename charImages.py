from math import gcd

import numpy as np
from PIL import Image


class image:
    def __init__(self, image, x0, y0, x1, y1, step=None, chars=None):
        im = np.array(Image.open(f"{image}"), dtype="uint8")
        self.height = y1 - y0
        self.width = x1 - x0
        self.step = step
        if chars is None:
            self.chars = [".", ",", "^", "*", ";", "&", "#", "@"]
        if step is None:
            self.step = gcd(self.height, self.width)
        if not self.check_image(len(im), len(im[0])):
            raise ValueError(
                f"Something is wrong, please re-enter values\nDimensions are: {len(im[0])}x{len(im)}, step={self.step}")
        self.image = im[y0: y1, x0: x1]

    def check_image(self, pich, picw):
        return picw >= self.width > 0 and pich >= self.height > 0 and self.height % self.step == 0 == self.width % self.step

    def gray_scale(self):
        def gray(x):
            return (x[0] * 0.2989) + (x[1] * 0.5870) + (x[2] * 0.1140)
        return np.apply_along_axis(gray, 2, self.image)

    def chunks(self):
        def avg(x, i, j, s):
            return x[i: i + s, j: j + s].mean()

        ret = []
        [ret.append([avg(self.image, i, j, self.step) for j in range(0, self.width, self.step)]) for i in
         range(0, self.height, self.step)]
        return np.array(ret)

    def generate_image(self):
        def to_chr(x):
            return np.array([self.chars[int(a / 255.0 * len(self.chars))] for a in x])
        return np.apply_along_axis(to_chr, 0, np.array(self.image))

    def print_image(self):
        [print(' '.join(l)) for l in self.image.tolist()]

    def write_to_file(self, file_name):
        with open(f"{file_name}.txt", 'w') as f:
            for i in range(self.height):
                for j in range(self.width):
                    f.write(self.image[i][j] + " ")
                f.write("\n")

    def show(self):
        Image.fromarray(self.image).show()

    def convert(self):
        self.image = self.gray_scale()
        self.image = self.chunks()
        self.image = self.generate_image()


x0 = 0
y0 = 0
x1 = 1500
y1 = 1300
step = 10

fname = "eilonimg.png"
im = image(fname, x0, y0, x1, y1)
im.convert()
im.print_image()
