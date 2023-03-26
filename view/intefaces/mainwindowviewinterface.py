from common.functions import abstract

from PySide2 import QtCore, QtGui, QtWidgets


class MainWindowViewInterface(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Signals
        self.videoIndexChangedSignal = QtCore.Signal(int)
        self.keywordClickedSignal = QtCore.Signal(str)
        self.keywordDoubleClickedSignal = QtCore.Signal(str)

    @abstract
    def setContext(self, context: str):
        pass

    def removeWordFromWords
