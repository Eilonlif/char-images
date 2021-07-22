from PIL import Image
import numpy as np
import math


def generateimage(image, step, chars):
    newImage = []
    for i in range(0, len(image), step):
        newImage.append([])
        a = 0
        for j in range(0, len(image[0]), step):
            s = 0
            for a in range(i, i + step):
                for b in range(j, j + step):
                    s += image[a][b]
            try:
                a = s / math.pow(step, 2)
            except TypeError:
                pass
            newImage[int(i / step)].append(chars[math.floor((float(a) / 255.0) * float(len(chars))) - 1])
    return newImage


def tograyscale(image):
    gs = []
    for i in range(len(image)):
        gs.append([])
        for j in range(len(image[0])):
            gs[i].append(int((image[i][j][0] * 0.2989) + (image[i][j][1] * 0.5870) + (image[i][j][2] * 0.1140)))
    return gs


def printimage(image):
    for i in range(len(image)):
        for j in range(len(image[i])):
            print(image[i][j], end=" ")
        print()


def writetofile(fileName, image):
    with open(f"{fileName}.txt", 'w') as f:
        for i in range(len(image)):
            for j in range(len(image[i])):
                f.write(image[i][j] + " ")
            f.write("\n")


def show(image):
    Image.fromarray(image).show()


fname = "f.jpg"  # Your image file name (with image type)
try:
    image = np.array(Image.open(f"{fname}"), dtype="uint8")
except FileNotFoundError as err:
    print(err)
    quit()

chars = [".", ",", "^", "*", ";", "&", "#", "@"]
startx = 0
starty = 0
endx = 800
endy = 800
step = 8

if startx < 0 or starty < 0 or endy >= len(image) or endy >= len(image[0]) or endx < startx or endy < starty or (endx - startx) % step != 0 or (endy - starty) % step != 0:
    print("Something is wrong, please re-enter values")
    quit()

image = image[starty: endy, startx: endx]   # Re-sizing the image
image = tograyscale(image)                  # Gray-scaling the image
image = generateimage(image, step, chars)   # Generating char image
printimage(image)                           # Printing char image
writetofile(f"{fname}_char_image", image)   # Writing to a file
