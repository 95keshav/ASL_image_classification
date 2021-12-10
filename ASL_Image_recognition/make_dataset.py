import cv2
import os
import env
import pandas as pd
import numpy as np
from random import shuffle
import shutil
from PIL import Image
from keras.utils import np_utils
from matplotlib import pyplot as plt


class ImagePrepareDataset:
    def __init__(self, base_path, img_limit):
        try:
            if base_path:
                if type(img_limit).__name__ == "int":
                    print("initiated")
                    self.basepath = base_path
                    self.img_limit = int(img_limit)
                    self.dir = os.listdir(self.basepath)
                    self.inner_dir = os.listdir(
                        os.path.join(self.basepath, self.dir[0])
                    )
                else:
                    self.img_limit = 1
        except Exception as e:
            print(e)

    def down_size_processing(self, size=(64, 64)):
        print("going through dirs")
        for person in self.dir[:-1]:
            print(person)
            for letter in self.inner_dir:
                print(letter)
                no_of_images = 0
                for image in os.listdir(os.path.join(self.basepath, person, letter)):
                    image_ext = image.split(".")
                    image = Image.open(
                        os.path.join(self.basepath, person, letter, image)
                    )
                    image = image.resize(size)
                    no_of_images += 1
                    filename = f"{person}_{letter}_{no_of_images}.{image_ext[1]}"
                    train_path = os.path.join(self.basepath, "training", letter)
                    if not os.path.exists(train_path):
                        os.makedirs(train_path)
                    image.save(os.path.join(train_path, filename))
                    print(filename)
                    if no_of_images > self.img_limit:
                        break

    def shuffle_images(self, total_images):
        for letter in self.inner_dir:
            train_path = os.path.join(self.basepath, "training_shuffleV2_0_200", letter)
            train_path_shuffle = os.path.join(
                self.basepath, "training_shuffleV2_200_400", letter
            )
            if not os.path.exists(os.path.join(train_path_shuffle, letter)):
                os.makedirs(os.path.join(train_path_shuffle, letter))
            images_names = os.listdir(train_path)
            # shuffle(images_names)
            for img_name in images_names[total_images:]:
                fname = os.path.join(train_path, img_name)
                fnamedist = os.path.join(train_path_shuffle, img_name)
                nname = os.path.join(
                    train_path_shuffle,
                    f"{letter}_{images_names.index(img_name)}.png",
                )
                os.chmod(train_path, 777)
                os.chmod(train_path_shuffle, 777)
                shutil.copyfile(fname, fnamedist)
                os.rename(fnamedist, nname)
                os.remove(fname)
                print(nname)

    def copyPaste(self):
        for letter in self.inner_dir:
            copy_path = os.path.join(
                self.basepath, "training_shuffleV2_200_400", letter
            )
            paste_path = os.path.join(self.basepath, "training_shuffle_400", letter)
            images_names = os.listdir(copy_path)
            i = 200
            for img_name in images_names:
                fname = os.path.join(copy_path, img_name)
                fnamedist = os.path.join(paste_path, img_name)
                nname = os.path.join(paste_path, f"{letter}_{i}.png")
                i = i + 1
                os.chmod(copy_path, 777)
                os.chmod(paste_path, 777)
                shutil.copyfile(fname, fnamedist)
                os.rename(fnamedist, nname)
                print(nname)


BASEPATH = "dataset"
IMAGE_COUNT = 500

preprocessing = ImagePrepareDataset(BASEPATH, IMAGE_COUNT)
# preprocessing.down_size_processing()
# preprocessing.shuffle_images(total_images=200)
preprocessing.copyPaste()
