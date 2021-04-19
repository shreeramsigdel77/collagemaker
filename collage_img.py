

# -*- coding: utf-8 -*-

"""

Collage maker - tool to create picture collages

Author: Delimitry

"""


import argparse

import os

import random

from PIL import Image

def make_collage(images, filename, width, height, init_height,count):

    """

    Make a collage image with a width equal to `width` from `images` and save to `filename`.

    """

    if not images:

        print('No images for collage found!')

        return False

    margin_size = 2

    # run until a suitable arrangement of images is found

    while True:

        # copy images to images_list

        images_list = images[:]

        coefs_lines = []

        images_line = []

        x = 0

        while images_list:

            # get first image and resize to `init_height`

            img_path = images_list.pop(0)

            img = Image.open(img_path)

            img.thumbnail((width, init_height))

            # when `x` will go beyond the `width`, start the next line

            if x > width:

                coefs_lines.append((float(x) / width, images_line))

                images_line = []

                x = 0

            x += img.size[0] + margin_size

            images_line.append(img_path)

        # finally add the last line with images

        coefs_lines.append((float(x) / width, images_line))

        # compact the lines, by reducing the `init_height`, if any with one or less images

        if len(coefs_lines) <= 1:

            break

        if any(map(lambda c: len(c[1]) <= 1, coefs_lines)):

            # reduce `init_height`

            init_height -= 10

        else:

            break
    # get output height

    out_height = 0

    for coef, imgs_line in coefs_lines:

        if imgs_line:

            # out_height += int(init_height / coef) + margin_size
            out_height = height
           
    if not out_height:

        print('Height of collage could not be 0!')

        return False

    collage_image = Image.new('RGB', (width, int(out_height)), (35, 35, 35))

    # put images to the collage

    y = 0
   
    for coef, imgs_line in coefs_lines:

        if imgs_line:

            x = 0

            for img_path in imgs_line:

                img = Image.open(img_path)

                # if need to enlarge an image - use `resize`, otherwise use `thumbnail`, it's faster

                k = (init_height / coef) / img.size[1]

                if k > 1:

                    # img = img.resize((int(img.size[0] * k), int(img.size[1] * k)), Image.ANTIALIAS)
                    img = img.resize((512, 512), Image.ANTIALIAS)
                    

                else:

                    img.thumbnail((int(width / coef), int(init_height / coef)), Image.ANTIALIAS)

                if collage_image:

                    collage_image.paste(img, (int(x), int(y)))

                x += img.size[0] + margin_size
            if y<513:
                y += int(init_height / coef) + margin_size
                
    collage_image.save(filename+str(count)+'.jpg')
    return True

def main():


    input_folder = "/home/pasonatech/labelme/collage_img-maker/folder1"
    output_folder = "/home/pasonatech/labelme/collage_img-maker/collage_output/"
    output_width = 512
    output_height = 512
    init_height = 128 #minimize the number for dense collage, maximize for low frequency
    shuffle = True
    total_image = 1000

    # get images

    files = [os.path.join(input_folder, fn) for fn in os.listdir(input_folder)]

    images = [fn for fn in files if os.path.splitext(fn)[1].lower() in ('.jpg', '.jpeg', '.png')]

    if not images:

        print('No images for making collage! Please select other directory with images!')

        exit(1)


    # shuffle images if needed

    if shuffle:

        random.shuffle(images)

    for i in range(total_image):    

        imagesRandom = random.choices(images,k=50)


        print('Making collage...')

        res = make_collage(imagesRandom, output_folder, output_width,output_height, init_height,i)

        if not res:

            print('Failed to create collage!')

            exit(1)

        print(f'Collage {i} is ready!')


if __name__ == '__main__':

    main()

    

