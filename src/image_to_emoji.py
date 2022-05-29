#!/usr/local/bin/python3

import time
import numpy as np
import cv2


class ImageToEmoji():
    def __init__(self, path: str = None):
        self.path = path

    def rand_arr(size):
        return np.random.randint(0, 256, size*size)

    def resize_image(self, image, scale):
        scale_percent = scale  # percent of original size
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        # resize image
        resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        return resized

    # level should be 0 - 1

    def shadow_by_level(self, level):
        # shadows = ['😁', '🫠', '🥶', '😊', '🙂', '👨‍💻', '🫥']
        shadows = ['🫥', '🖤', '🤎', '💜', '💙', '🧡',
                   '❤️', '💚', '💖', '💛', '😊', '🤍', '❤️‍🔥', ]
        # shadows = ['💣', '💥', '🍑', '❤️', '😏', '🔥']
        part = 1 / len(shadows)
        return {self.shadow_key(i, level, part, len(shadows)): shadows[i] for i in range(len(shadows))}[True]

    def shadow_key(self, index, level, part, size):
        if index == 0:
            return level <= 1 * part
        elif index == size:
            return part * index <= level
        else:
            return part * index < level < size

    def fill_arr_with_emoji(self, backtorgb):
        arr = []
        for h in backtorgb:
            for w in h:
                if w[0] == w[1] == w[2]:
                    greyLevel = w[0] / 255
                    arr.insert(0, self.shadow_by_level(greyLevel))
        return arr

    def process_and_save(self, scale: int = 50, toSave: bool = False):
        arrAndWidth = self.convert_image_to_emoji(scale=scale)
        if toSave:
            t = time.process_time()
            self.save_to_file(arrAndWidth[0], arrAndWidth[1])
            elapsed_time = time.process_time() - t
            print(f'Elapsed time: {elapsed_time}ms')

    def convert_image_to_emoji(self, scale: int = 50) -> tuple:
        print(f'convert_image_to_emoji = {self.path}')
        img = cv2.imread(self.path)
        resizedImg = self.resize_image(img, scale)
        gray = cv2.cvtColor(resizedImg, cv2.COLOR_BGR2GRAY)
        backtorgb = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
        height, width = backtorgb.shape[:2]
        print(f'Original Dimensions : height={height}, width={width}')
        return [self.fill_arr_with_emoji(backtorgb), width]

    def save_to_file(self, arr: list[str], width) -> int:
        arrLength = len(arr)
        if (width == None) & (arrLength == 0):
            return -1
        with open('bytearray.txt', 'w') as file:
            for index in range(arrLength):
                safeIndex = index if (index < arrLength) & (
                    index != 0) else arrLength
                i = arrLength - safeIndex
                try:
                    isNewLine = (i != 0) & ((i - 1) % width == 0)
                    strToSave = arr[i] + ("\n" if isNewLine else " ")
                    file.write(strToSave)
                except IndexError:
                    print(
                        f'Failed with i = {i} and arrLength = {arrLength} and index = {index} safeIndex = {safeIndex}')
                    return -1
        return 0

    def arr_to_string(self, arr: list[str], width: int = 0) -> str:
        if not arr:
            return ""
        arrLength = len(arr)
        if (width > 0) & (arrLength == 0):
            return ""
        resultStr = ""
        for index in range(arrLength):
            safeIndex = index if (index < arrLength) & (
                index != 0) else arrLength
            i = arrLength - safeIndex
            try:
                isNewLine = (i != 0) & ((i - 1) % width == 0)
                strToSave = arr[i] + ("\n" if isNewLine else " ")
                resultStr += strToSave
            except IndexError:
                print(
                    f'Failed with i = {i} and arrLength = {arrLength} and index = {index} safeIndex = {safeIndex}')
                return ""
            except ZeroDivisionError:
                print(
                    f'Failed with i = {i} and arrLength = {arrLength} and index = {index} safeIndex = {safeIndex}')
                return ""
        return resultStr


def main_image_to_emoji():
    imageToEmoji = ImageToEmoji(
        path='/Users/user/PythonProjects/image_to_emoji/example1.png')
    imageToEmoji.path = '/Users/user/PythonProjects/image_to_emoji/example5.png'
    imageToEmoji.process_and_save(scale=25, toSave=True)
    del imageToEmoji


# main_image_to_emoji()
