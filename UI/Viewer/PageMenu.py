from PyQt5.QtWidgets import QListWidget


class PageMenu(QListWidget):
    def __init__(self):
        self.listener = None
        self.__table = dict()  # index: string
        super().__init__()  # QListWidget
        super().itemClicked.connect(self.__click_listener)

    def addItem(self, index):
        """
        @type index: int
        """
        super().addItem('page ' + str(index))
        self.__table['page ' + str(index)] = index

        if super().count() == 1:
            super().setCurrentRow(0)
            if self.listener:
                self.listener(index)

    def __click_listener(self):
        index = super().currentItem().text()
        self.listener(self.__table[index])

    def currentItem(self):
        return super().currentItem()
