import requests

from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class ImageViewer(QLabel):
    def __init__(self):
        super().__init__()
        self.__orig_pixmap = QPixmap()
        self.__now_pixmap = None
        self.__height = 0
        self.__width = 0

    def loadFromData(self, index, url):
        response = requests.get(url)
        if response.status_code != 200:
            print('[PageMenu] status code: ' + str(response.status_code))
            return False

        self.__orig_pixmap.loadFromData(response.content)
        self.__now_pixmap = self.__orig_pixmap
        self.__height = self.__orig_pixmap.height()
        self.__width = self.__orig_pixmap.width()
        super().setPixmap(self.__now_pixmap)
        return True

    def height(self):
        return self.__height

    def width(self):
        return self.__width

    def resize(self, height, width):
        self.__now_pixmap = self.__now_pixmap.scaled(height, width, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.__heigth = self.__now_pixmap.height()
        self.__width = self.__now_pixmap.width()
        super().setPixmap(self.__now_pixmap)

    def reset(self):
        self.__now_pixmap = self.__orig_pixmap
        self.__heigth = self.__now_pixmap.height()
        self.__width = self.__now_pixmap.width()
        super().setPixmap(self.__now_pixmap)
