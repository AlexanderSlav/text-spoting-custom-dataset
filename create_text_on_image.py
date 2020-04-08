import cv2
import numpy as np
import argparse
import random
import json
import os
import re
from PIL import ImageFont, ImageDraw, Image

#set numpy set for reproducability
np.random.seed(42)

default_random_words = ['Всех','победим']

def overlay_texts(image, x, y, text):

    b, g, r, a = 0, 0, 0, 0

    fontpath = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"  #
    font = ImageFont.truetype(fontpath, 48)
    img_pil = Image.fromarray(image)
    draw = ImageDraw.Draw(img_pil)
    draw.text((x, y), text, font=font, fill=(b, g, r, a))
    size = draw.textsize(text, font=font)

    img = np.array(img_pil)

    return img, size[0], size[1]


def show_image(name, image):
    cv2.imshow(name, image)
    while True:
        key = cv2.waitKey(1)
        if key == 27:
            cv2.destroyAllWindows()  # ESC key to break
            break


def get_random_coordinates_of_text(line):

    top_padding    = 100
    bottom_padding = 50

    pixel_per_line = int((opt.height - top_padding - bottom_padding) / opt.words_per_image)

    x = random.randrange(50, int(opt.width * 3 / 4))
    y = pixel_per_line * line + top_padding

    return x, y

def write_json_file(data,file_name):
    with open(file_name, 'w',encoding="utf-8") as outfile:
        json.dump(data, outfile, ensure_ascii=False)


def make_dict_for_annotations():
        data = {}
        data['type'] = 'instances'
        data['images'] = []
        data['annotations'] = []
        data['categories'] = [{
            'supercategory': 'none',
            'name': 'text',
            'id': 1
        }]
        return data

def add_image_object_to_data(data, image_name, id):
    data['images'].append(
    {
        'file_name': image_name,
        'height': opt.height,
        'width': opt.width,
        'id': id
    })

def add_annotations_object_to_data(data, x1, y1, w, h, text, idx, image_id, area):

    data['annotations'].append({

        'bbox':[x1, y1, w + 1, h + 1],
        'segmentation':[[x1 + w, y1 + h, x1, y1 + h, x1, y1, x1 + w, y1]],

        'text':{
            "transcription": text,
            "legible": 1,
            "language": "english"
        },
        "ignore": 0,
        "id": idx,
        "image_id": image_id,
        "area": area,
        "iscrowd": 0,
        "category_id": 1
        }
    )

def main(opt):

    random_words = []

    if opt.dictionary != None:
        # read from file here
        f = open(opt.dictionary, "r", encoding="utf-8")
        rawdata = f.read()

        dict_words = re.split(r'[ ,.!?():;\[\]\n]+',rawdata.lower())

        for i in range(opt.num_of_images*opt.words_per_image):

            idx = random.randint(0, len(dict_words) - 1)
            while (len(dict_words[idx]) < 5) or ('"' in dict_words[idx]) or ('-' in dict_words[idx]):
                idx = random.randint(0, len(dict_words) -1)

            random_words.append(dict_words[idx])

    else:
        random_words = default_random_words
        num_words = len(random_words)
        opt.words_per_image = 1

    data = make_dict_for_annotations()

    color = (0, 0, 0)
    font = cv2.FONT_HERSHEY_DUPLEX

    for i in range(opt.num_of_images):

        add_image_object_to_data(data, f'{opt.path}/{i}_sample.jpg', i)
        new_image = 255 * np.ones(shape=[opt.height, opt.width, 3], dtype=np.uint8)

        for j in range(opt.words_per_image):

            size = random.randrange(1, 5)
            x1, y1 = get_random_coordinates_of_text(j)

            idx = i*opt.words_per_image + j

            new_image, w, h = overlay_texts(new_image, x1, y1, random_words[idx])

            add_annotations_object_to_data(data,
                                           x1, y1, w, h,
                                           random_words[idx],
                                           idx,
                                           i,
                                           w * h)

        if opt.save:
            cv2.imwrite(os.path.join(opt.path, f'{i}_sample.jpg'), new_image)
        if opt.show:
            show_image("Created Image", new_image)
    write_json_file(data, opt.file_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-w_im', '--width', type=int, default=300, help="width of new image")
    parser.add_argument('-h_im', '--height',type=int, default=300, help="height of new image")
    parser.add_argument('-n', '--num_of_images',type=int, default=3, help="samples to generate amount")
    parser.add_argument('-words', '--words_per_image',type=int, default=1, help="words_per_image")

    parser.add_argument('-path', '--path',type=str, default="", help="dir to save generated images")
    parser.add_argument('-dict', '--dictionary',type=str, default=None, help="source for dictionary")
    parser.add_argument('-f', '--file_name',type=str, default='annotations.json', help="annotations file")
    parser.add_argument('-s', '--save', action='store_true')

    parser.add_argument('--show', action='store_true')
    opt = parser.parse_args()
    main(opt)
