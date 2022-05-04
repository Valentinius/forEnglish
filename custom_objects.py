from PySide2 import QtCore, QtGui, QtWidgets


class EditPanel(QtWidgets.QWidget):
    def __init__(self, title: str, label_width: int, ledit_width: int,
                 block_height: int = 20, parent: QtWidgets.QWidget = None,
                 orientation: QtCore.Qt.Orientation = QtCore.Qt.Horizontal,
                 input_box: QtWidgets = QtWidgets.QLineEdit):
        super(EditPanel, self).__init__(parent)

        self.title = title
        self._label_width = label_width
        self._ledit_width = ledit_width
        self._block_height = block_height
        self._orientation = orientation
        self._input_box = input_box
        self.value = None

        self._init_ui()

    def _init_ui(self):
        main_layout = (QtWidgets.QVBoxLayout(self)
                       if self._orientation == QtCore.Qt.Vertical else QtWidgets.QHBoxLayout(self))

        label = QtWidgets.QLabel(self.title, self)
        label.setFixedWidth(self._label_width)
        label.setAlignment(QtCore.Qt.AlignCenter)

        self.text_box = self._input_box()
        self.text_box.setMinimumWidth(self._ledit_width)
        self.text_box.setMinimumHeight(self._block_height)

        main_layout.addWidget(label)
        main_layout.addWidget(self.text_box)
