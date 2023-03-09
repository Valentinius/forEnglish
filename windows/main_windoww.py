from PySide2 import QtCore, QtGui, QtWidgets
from custom_objects import EditPanel
from videos import Videos


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.videos = Videos()

        self.setWindowTitle('Ищем слова для английского')
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)

        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QtWidgets.QHBoxLayout()

        # Настраиваем левую часть с настройками
        label_width = 300
        ledit_width = 300
        settings_splitter = QtWidgets.QSplitter(QtGui.Qt.Vertical)

        self.video_selector_combobox = EditPanel('Выберите видео', label_width, ledit_width,
                                                 orientation=QtGui.Qt.Vertical,
                                                 input_box=QtWidgets.QComboBox)
        self.add_video_button = QtWidgets.QPushButton('Добавить видео')
        self.remove_video_button = QtWidgets.QPushButton('Удалить видео')
        self.save_words_button = QtWidgets.QPushButton('Сохранить')
        self.load_videos_data_button = QtWidgets.QPushButton('Загрузить')

        add_delete_buttons_splitter = QtWidgets.QSplitter(QtGui.Qt.Horizontal)
        add_delete_buttons_splitter.addWidget(self.add_video_button)
        add_delete_buttons_splitter.addWidget(self.remove_video_button)

        save_load_buttons_splitter = QtWidgets.QSplitter(QtGui.Qt.Horizontal)
        save_load_buttons_splitter.addWidget(self.save_words_button)
        save_load_buttons_splitter.addWidget(self.load_videos_data_button)

        settings_splitter.addWidget(self.video_selector_combobox)
        settings_splitter.addWidget(add_delete_buttons_splitter)
        settings_splitter.addWidget(save_load_buttons_splitter)

        main_layout.addWidget(settings_splitter)

        # Окна с выводом информации
        windows_splitter = QtWidgets.QSplitter(QtGui.Qt.Vertical)

        self.context_list = QtWidgets.QListWidget()
        self.words_list = QtWidgets.QListWidget()
        self.keywords_list = QtWidgets.QListWidget()

        words_splitter = QtWidgets.QSplitter(QtGui.Qt.Horizontal)
        words_splitter.addWidget(self.words_list)
        words_splitter.addWidget(self.keywords_list)

        windows_splitter.addWidget(self.context_list)
        windows_splitter.addWidget(words_splitter)

        main_layout.addWidget(windows_splitter, 2)

        # Остальные настройки
        main_widget.setLayout(main_layout)
        self._set_events()

    def _set_events(self):
        """
        Функция устанавливает события.

        :return:
        """
        self.video_selector_combobox.text_box.currentIndexChanged.connect(self._video_changed)
        self.words_list.itemDoubleClicked.connect(self._word_double_clicked)
        self.words_list.itemClicked.connect(self._word_clicked)
        self.keywords_list.itemDoubleClicked.connect(self._keyword_double_clicked)
        self.keywords_list.itemClicked.connect(self._word_clicked)

        self.save_words_button.clicked.connect(self._save_button_clicked)
        self.add_video_button.clicked.connect(self._add_button_clicked)
        self.remove_video_button.clicked.connect(self._remove_button_clicked)
        self.load_videos_data_button.clicked.connect(self._load_videos_data_button_clicked)

    def _video_changed(self, idx):
        """
        Функция определяет, что должно происходить при смене видео.

        :param idx: индекс нового выбранного видео.
        :return:
        """
        if idx > -1:
            self._save_keywords()
            self.words_list.clear()
            self.keywords_list.clear()
            self.words_list.addItems(word for word in self.videos[idx].words if word not in self.videos[idx].keywords)
            self.keywords_list.addItems(self.videos[idx].keywords)

    def _word_double_clicked(self, item):
        """
        Функция определяет действия после двойного нажатия мышью на слово в окне слов.

        :param item: контейнер с выбранным словом.
        :return:
        """
        self.keywords_list.addItem(item.text())
        self.words_list.takeItem(self.words_list.currentRow())

    def _keyword_double_clicked(self, item):
        """
        Функция определяет действия после двойного нажатия мышью на слово в окне ключевых слов.

        :param item: контейнер с выбранным словом.
        :return:
        """
        self.words_list.addItem(item.text())
        self.keywords_list.takeItem(self.keywords_list.currentRow())

    def _word_clicked(self, item):
        """
        Функция определяет действия, происходящие после однократного нажатия на слова в окнах слов и ключевых слов.

        :param item: контейнер с выбранным словом.
        :return:
        """
        self.context_list.clear()

        idx = self.video_selector_combobox.text_box.currentIndex()
        word = item.text()
        sentences = self.videos[idx].correct_video_sentences
        #text = self.videos[idx].text

        sentences_idx = self.videos[idx].indexes[self.videos[idx].words.index(word)];

        for item in sentences_idx:
            self.context_list.addItem(sentences[item])

        #pos = text.find(word)
        #while pos > -1:
        #    find_start = pos + 1
        #    start = pos - 50 if pos >= 50 else 0
        #    end = pos + 50 if pos + 50 < len(text) else len(text)
        #    self.context_list.addItem(f'<b>{text[start:end]}</b>')
        #    pos = text.find(word, find_start)

    def _add_button_clicked(self):
        """
        Функция вызывает окно добавления видео. Затем добавляет это видео в список.

        :return:
        """
        # https://www.youtube.com/watch?v=C72WkcUZvco
        # https://www.youtube.com/watch?v=R_gFhRsWLMw
        # https://www.youtube.com/watch?v=mQeplLGXIY4&list=PLXC_gcsKLD6n7p6tHPBxsKjN5hA_quaPI&index=4
        # https://www.youtube.com/watch?v=OUp7ale49lI&list=PLXC_gcsKLD6n7p6tHPBxsKjN5hA_quaPI&index=4
        # https://www.youtube.com/watch?v=BN8pC91rJaU&list=PLXC_gcsKLD6n7p6tHPBxsKjN5hA_quaPI&index=6
        url, ok = QtWidgets.QInputDialog.getText(self, 'Добавить видео', 'Скопируйте ссылку с видео:')

        if ok:
            self.videos.add_video(url)
            self._videos_selector_update(len(self.videos) - 1)

    def _remove_button_clicked(self):
        """
        Функция удаляет видео из списка видео.

        :return:
        """
        idx = self.video_selector_combobox.text_box.currentIndex()
        del self.videos[idx]
        self.words_list.clear()
        self.keywords_list.clear()
        self._videos_selector_update(idx)

    def _save_button_clicked(self):
        """
        Функция сохраняет информацию о видео после нажатия на кнопку 'Сохранить'.

        :return:
        """
        reply = QtWidgets.QMessageBox.question(self, 'Сохранение', 'Вы уверены, что хотите перезаписать?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self._save_keywords()
            self.videos.save('data.pickle')

    def _load_videos_data_button_clicked(self):
        """
        Функция загружает список видео из файла.

        :return:
        """
        self.videos.load('data.pickle')
        self._videos_selector_update()

    def _videos_selector_update(self, idx: int = 0):
        """
        Функция обновляет список видео. Вызывается в функциях, где он изменяется.

        :param idx: строка, которую необходимо выбрать после обновления.
        :return:
        """
        self.video_selector_combobox.text_box.clear()
        self.video_selector_combobox.text_box.addItems(self.videos.get_names())
        if len(self.videos) > 0:
            self.video_selector_combobox.text_box.setCurrentIndex(idx if idx < len(self.videos) else 0)

    def _save_keywords(self):
        """
        Функция сохраняет ключевые слова и список вопросов.

        :return:
        """
        idx = self.video_selector_combobox.text_box.currentIndex()
        self.videos[idx].keywords = set([self.keywords_list.item(i).text()
                                         for i in range(self.keywords_list.count())])
