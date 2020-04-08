import cv2
import numpy as np
import argparse
import random
import json
import os
import re
from PIL import ImageFont, ImageDraw, Image

def overlay_texts(image, x, y, text, font):

    b, g, r, a = 0, 0, 0, 0


    img_pil = Image.fromarray(image)
    draw = ImageDraw.Draw(img_pil)
    draw.text((x, y), text, font=font, fill=(b, g, r, a))
    size = draw.textsize(text, font=font)

    img = np.array(img_pil)

    return img

def show_image(name, image):
    cv2.imshow(name, image)
    while True:
        key = cv2.waitKey(1)
        if key == 27:
            cv2.destroyAllWindows()  # ESC key to break
            break


def get_random_coordinates_of_text(line, total):

    top_padding    = 50
    bottom_padding = 50

    pixel_per_line = int((opt.height - top_padding - bottom_padding) / total)

    x = random.randrange(50, 100)
    y = pixel_per_line * line + top_padding

    return x, y


def get_product_name_text_coordinates():
    x = 10
    y = 10
    return x, y


def get_price_text_coordinates():
    x = 5
    y = 5
    return x, y



def main(opt):
    if opt.words:
        words = opt.words.split("<")

        new_image = 255 * np.ones(shape=[opt.height, opt.width, 3], dtype=np.uint8)

        for idx in range(len(words)):

            x1, y1 = get_random_coordinates_of_text(idx, len(words))
            new_image = overlay_texts(new_image, x1, y1, words[idx])
    elif opt.product_name and opt.price:
        product_names_line1 = ['Молоко обезжиренное 50г','Бананы весовые 100мл','Творог городецкий 800г',
                         'Йогурт вкусный 500мл','Хлопья овсяные 1кг','Мука пшеничная 150кг',
                         'Яблоки сезонные 1л','Апельсины отборные 2кг', 'Помидоры домашние 900г', 'Хлеб бездрожевой 100кг']

        product_names_line2 = ['настоящее точно','какие то сушки','саша не разрешил',
                         'купить мне сушки','очень вкусные','что еще придумать',
                         'вторая строка','отборные точно', 'домашние', 'бездрожевой']


        for i in range(len(product_names_line2)):

            line1_idx = random.randint(0, len(product_names_line2)-1)
            line2_idx = random.randint(0, len(product_names_line2) - 1)

            price = str(random.randrange(9, 10))
            new_image = 255 * np.ones(shape=[opt.height, opt.width, 3], dtype=np.uint8)
            fontpath = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"  #
            font_line1 = ImageFont.truetype(fontpath, 35)
            font_line2 = ImageFont.truetype(fontpath, 20)
            price_font = ImageFont.truetype(fontpath, 220)

            pr_name_x, pr_name_y = get_product_name_text_coordinates()
            ##new_image = overlay_texts(new_image, pr_name_x, pr_name_y, product_names_line1[line1_idx], font_line1)
            ##new_image = overlay_texts(new_image, pr_name_x, pr_name_y + 50, product_names_line2[line2_idx], font_line2)

            price_x, price_y = get_price_text_coordinates()
            new_image = overlay_texts(new_image, price_x, price_y, price, price_font)

            price_x, price_y = get_price_text_coordinates()
            #new_image = overlay_texts(new_image, price_x + 200, price_y + 25, "99", font_line1)
            #new_image = overlay_texts(new_image, price_x + 200, price_y + 65, "р/шт", font_line2)

            if opt.show:
                show_image("Created Image", new_image)
            else:
                cv2.imwrite(f'images/text_for_price_tag{i}.png', new_image)

    else:
        print('Wrong arguments format!')
        return

    if opt.file_name:
        cv2.imwrite(opt.file_name, new_image)
    if opt.show:
        show_image("Created Image", new_image)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-w_im', '--width', type=int, default=480, help="width of new image")
    parser.add_argument('-h_im', '--height',type=int, default=320, help="height of new image")
    parser.add_argument('-words', '--words',type=str, default="", help="text to print")
    # parser.add_argument('-p_name', '--product_name', type=str, default="Молоко Обезжиренное",
    #                     help="text to print")
    # parser.add_argument('-price', '--price', type=str, default="80 99",
    #                     help="text to print")
    parser.add_argument('-p_name', '--product_name', action='store_true')
    parser.add_argument('-price', '--price', action='store_true')
    parser.add_argument('-f', '--file_name', type=str, default='temp.jpg', help="name of output file")
    parser.add_argument('--show', action='store_true')

    opt = parser.parse_args()

    main(opt)
