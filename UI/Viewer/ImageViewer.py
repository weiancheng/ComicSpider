from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap

import os
import requests


class ImageViewer(QLabel):
    def __init__(self):
        super().__init__()
        self.__pixmap = None
        self.__current_pixmap = None

    def load_from_url(self, url):
        response = requests.get(url)
        if response.status_code != requests.codes.ok:
            print('[Error] URL: ' + url + ' is not valid')
            return -1

        self.__pixmap = QPixmap()
        self.__pixmap.loadFromData(response.content)
        self.__current_pixmap = self.__pixmap
        super().setPixmap(self.__current_pixmap)
        return 0

    def load_from_local(self, path):
        if not os.path.exists(path):
            print("[Error] file " + path + " is not exist")
            return -1

        self.__pixmap = QPixmap(path)
        self.__current_pixmap = self.__pixmap
        super().setPixmap(self.__current_pixmap)
        return 0

    def resize(self, height, width):
        if not self.__pixmap:
            return -1

        self.__current_pixmap = self.__pixmap.scaledToHeight(height)
        self.__current_pixmap = self.__current_pixmap.scaledToWidth(width)
        super().setPixmap(self.__current_pixmap)
        return 0

    def height(self):
        return self.__current_pixmap.height()

    def width(self):
        return self.__current_pixmap.width()

    def reset(self):
        self.__current_pixmap = self.__pixmap
        super().setPixmap(self.__current_pixmap)

