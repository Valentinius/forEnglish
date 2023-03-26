from model.intefaces.mainwindowmodelinterface import MainWindowModelInterface
from view.intefaces.mainwindowviewinterface import MainWindowViewInterface

from PySide2.QtCore import QObject, Signal, Slot


class MainWindowController(QObject):
    def __init__(self, view: MainWindowViewInterface, model: MainWindowModelInterface):
        self.view = view
        self.model = model
