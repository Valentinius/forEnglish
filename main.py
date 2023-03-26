import sys
import nltk

from PySide2 import QtWidgets
from windows.main_windoww import MainWindow
from styles import def_font


if __name__ == '__main__':
    nltk.download('stopwords')
    app = QtWidgets.QApplication(sys.argv)
    app.setFont(def_font)
    form = MainWindow()
    form.show()

    sys.exit(app.exec_())
