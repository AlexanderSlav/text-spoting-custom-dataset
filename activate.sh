source  /home/alexslav/Work/openvino_training_extensions/pytorch_toolkit/text_spotting/venv/bin/activate


rm -rf /home/alexslav/Work/openvino_training_extensions/pytorch_toolkit/text_spotting/text_spotting/datasets/data/coco/custom-ru/train
rm -rf /home/alexslav/Work/openvino_training_extensions/pytorch_toolkit/text_spotting/text_spotting/datasets/data/coco/custom-ru/test

mkdir /home/alexslav/Work/openvino_training_extensions/pytorch_toolkit/text_spotting/text_spotting/datasets/data/coco/custom-ru/train
mkdir /home/alexslav/Work/openvino_training_extensions/pytorch_toolkit/text_spotting/text_spotting/datasets/data/coco/custom-ru/test

python3 /home/alexslav/Work/text-spoting-custom-dataset/scipts/create_text_on_image.py -words 5 -n 10000 -w_im 1280 -h_im 768 -dict ../dicts/dict-azazel.txt -s -f /home/alexslav/Work/openvino_training_extensions/pytorch_toolkit/text_spotting/text_spotting/datasets/data/coco/train_annotations_ru.json -path /home/alexslav/Work/openvino_training_extensions/pytorch_toolkit/text_spotting/text_spotting/datasets/data/coco/custom-ru/train
python3 /home/alexslav/Work/text-spoting-custom-dataset/scipts/create_text_on_image.py -words 5 -n 20 -w_im 1280 -h_im 768 -dict ../dicts/dict-azazel.txt -s -f /home/alexslav/Work/openvino_training_extensions/pytorch_toolkit/text_spotting/text_spotting/datasets/data/coco/test_annotations_ru.json -path /home/alexslav/Work/openvino_training_extensions/pytorch_toolkit/text_spotting/text_spotting/datasets/data/coco/custom-ru/test
