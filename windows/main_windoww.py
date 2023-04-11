from PySide2 import QtCore, QtGui, QtWidgets
from custom_objects import EditPanel
from videos import Videos
import grammar_checker
#from video_data_2 import my_tool
import question_maker
#import random

class Ui_MainWindow(object):
    def __init__(self):
        self.centralwidget = None
        self.label = None
        #self.movie = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        #MainWindow.resize(250, 250)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # create label
        self.label = QtWidgets.QLabel(self.centralwidget)
        #self.label.setGeometry(QtCore.QRect(200, 200, 200, 200))
        #self.label.setMinimumSize(QtCore.QSize(200, 200))
        #self.label.setMaximumSize(QtCore.QSize(200, 200))
        self.label.setText("Please, wait while we loading video data")
        self.label.setObjectName("label")

        # add label to main window
        MainWindow.setCentralWidget(self.centralwidget)

        # set qmovie as label
        #self.movie = QtGui.QMovie("../loader.gif")
        #self.label.setMovie(self.movie)
        #self.movie.start()

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
        #settings_splitter = QtWidgets.QSplitter(QtGui.Qt.Vertical)
        settings_splitter = QtWidgets.QGroupBox()
        settings_splitter_layout = QtWidgets.QGridLayout()


        self.video_selector_combobox = EditPanel('Choose video:', label_width, ledit_width,
                                                 orientation=QtGui.Qt.Horizontal,
                                                 input_box=QtWidgets.QComboBox)
        self.add_video_button = QtWidgets.QPushButton('Add video')
        self.remove_video_button = QtWidgets.QPushButton('Delete video')
        self.save_words_button = QtWidgets.QPushButton('Save')
        self.load_videos_data_button = QtWidgets.QPushButton('Load')

        all_buttons_loader = QtWidgets.QGroupBox()
        all_buttons_loader_layout = QtWidgets.QGridLayout()

        all_buttons_loader_layout.addWidget(self.add_video_button, 0, 0)
        all_buttons_loader_layout.addWidget(self.remove_video_button, 0, 1)
        all_buttons_loader_layout.addWidget(self.save_words_button, 1, 0)
        all_buttons_loader_layout.addWidget(self.load_videos_data_button, 1, 1)

        all_buttons_loader.setLayout(all_buttons_loader_layout)

        #add_delete_buttons_splitter = QtWidgets.QSplitter(QtGui.Qt.Horizontal)
        #add_delete_buttons_splitter.addWidget(self.add_video_button)
        #add_delete_buttons_splitter.addWidget(self.remove_video_button)

        #save_load_buttons_splitter = QtWidgets.QSplitter(QtGui.Qt.Horizontal)
        #save_load_buttons_splitter.addWidget(self.save_words_button)
        #save_load_buttons_splitter.addWidget(self.load_videos_data_button)

        self.show_text_button = QtWidgets.QPushButton()
        self.show_text_button.setText("Show all text")


        settings_splitter_layout.addWidget(self.video_selector_combobox, 0, 0, 2, 1)
        settings_splitter_layout.addWidget(all_buttons_loader, 2, 0)
        #settings_splitter_layout.addWidget(add_delete_buttons_splitter, 2, 0)
        #settings_splitter_layout.addWidget(save_load_buttons_splitter, 3, 0)

        settings_splitter.setLayout(settings_splitter_layout)
        #main_layout.addWidget(settings_splitter)

        # Окна с выводом информации
        windows_splitter = QtWidgets.QSplitter(QtGui.Qt.Vertical)

        windows_splitter.addWidget(settings_splitter)

        self.current_sentence = 0
        self.all_sentences = 0
        self.sentences_idx = []
        self.sentences = []

        self.context_list = QtWidgets.QListWidget()
        self.words_list = QtWidgets.QListWidget()
        self.keywords_list = QtWidgets.QListWidget()
        self.keywords_list_2 = QtWidgets.QTextEdit()
        self.keywords_list_2.setReadOnly(True)
        self.label_count = QtWidgets.QLabel()
        self.label_count.setText(str(str(self.current_sentence) + "/" + str(self.all_sentences)))
        self.button_next = QtWidgets.QPushButton()
        self.button_previous = QtWidgets.QPushButton()
        self.button_next.setEnabled(False)
        self.button_next.setText("Next")
        self.button_previous.setEnabled(False)
        self.button_previous.setText("Previous")

        self.group_box_main = QtWidgets.QGroupBox()
        gb_main_layout = QtWidgets.QGridLayout()
        self.group_box_slave = QtWidgets.QGroupBox()
        gb_slave_layout = QtWidgets.QGridLayout()

        gb_main_layout.addWidget(self.keywords_list_2, 0, 0)
        gb_slave_layout.addWidget(self.label_count, 0, 0)
        gb_slave_layout.addWidget(self.button_previous, 0, 1)
        gb_slave_layout.addWidget(self.button_next, 0, 2)
        self.group_box_slave.setLayout(gb_slave_layout)
        gb_main_layout.addWidget(self.group_box_slave, 1, 0)
        self.group_box_main.setLayout(gb_main_layout)

        words_splitter = QtWidgets.QSplitter(QtGui.Qt.Horizontal)
        words_splitter.addWidget(self.words_list)
        words_splitter.addWidget(self.keywords_list)
        #words_splitter.addWidget()

        #windows_splitter.addWidget(self.context_list)
        windows_splitter.addWidget(QtWidgets.QLabel("Context:"))
        windows_splitter.addWidget(self.group_box_main)
        windows_splitter.addWidget(QtWidgets.QLabel("Words from video: "))
        windows_splitter.addWidget(words_splitter)

        self.show_text_button.setEnabled(False)
        windows_splitter.addWidget(self.show_text_button)

        main_layout.addWidget(windows_splitter, 2)

        questions_splitter = QtWidgets.QSplitter(QtGui.Qt.Vertical)

        sent_group_box = QtWidgets.QGroupBox()
        sent_group_box_layout = QtWidgets.QGridLayout()



        self.button_select_sentence_from_text = QtWidgets.QPushButton()
        self.button_select_sentence_from_text.setText("Get from context")

        label_question = QtWidgets.QLabel()
        label_question.setText("Sentence to question:")

        self.tb_sentence = QtWidgets.QTextEdit()

        self.button_check_grammar = QtWidgets.QPushButton()
        self.button_check_grammar.setText("Try to correct grammar")

        self.button_get_questions = QtWidgets.QPushButton()
        self.button_get_questions.setText("Get question")

        labol = QtWidgets.QLabel("Print your question here or try to make it above")
        self.tb_question = QtWidgets.QTextEdit()

        self.button_check_grammar_question = QtWidgets.QPushButton()
        self.button_check_grammar_question.setText("Try to correct grammar")

        self.button_save_question = QtWidgets.QPushButton()
        self.button_save_question.setText("Save question")

        sent_group_box_layout.addWidget(self.button_select_sentence_from_text, 0, 0)
        sent_group_box_layout.addWidget(self.button_check_grammar, 0, 1)
        sent_group_box_layout.addWidget(self.button_get_questions, 0, 2)

        sent_group_box.setLayout(sent_group_box_layout)


        #questions_splitter.addWidget(self.button_select_sentence_from_text)
        questions_splitter.addWidget(label_question)
        questions_splitter.addWidget(self.tb_sentence)
        #questions_splitter.addWidget(self.button_check_grammar)
        #questions_splitter.addWidget(self.button_get_questions)

        questions_splitter.addWidget(sent_group_box)

        questions_splitter.addWidget(labol)
        questions_splitter.addWidget(self.tb_question)

        ques_group_box = QtWidgets.QGroupBox()
        ques_group_box_layout = QtWidgets.QGridLayout()

        ques_group_box_layout.addWidget(self.button_check_grammar_question, 0, 0)
        ques_group_box_layout.addWidget(self.button_save_question, 0, 1)

        ques_group_box.setLayout(ques_group_box_layout)

        #questions_splitter.addWidget(self.button_check_grammar_question)
        #questions_splitter.addWidget(self.button_save_question)

        questions_splitter.addWidget(ques_group_box)

        self.questions_list = QtWidgets.QListWidget()
        self.delete_ques_button = QtWidgets.QPushButton()
        self.delete_ques_button.setEnabled(False)
        self.delete_ques_button.setText("Delete question")

        questions_splitter.addWidget(QtWidgets.QLabel("Your saved questions: "))
        questions_splitter.addWidget(self.questions_list)
        questions_splitter.addWidget(self.delete_ques_button)

        main_layout.addWidget(questions_splitter, 2)
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

        self.button_next.clicked.connect(self._next_button_clicked)
        self.button_previous.clicked.connect(self._previous_button_clicked)

        self.button_select_sentence_from_text.clicked.connect(self._button_select_sentence_from_text_clicked)
        self.button_check_grammar.clicked.connect(self._button_check_grammar_sentence_clicked)
        self.button_get_questions.clicked.connect(self._button_get_questions_clicked)
        self.button_check_grammar_question.clicked.connect(self._button_check_grammar_question_clicked)

        self.button_save_question.clicked.connect(self._save_ques_button_clicked)

        self.button_get_questions.setToolTip("Get question from current sentence")
        self.button_select_sentence_from_text.setToolTip("Get new sentence from context sentence")

        self.questions_list.itemDoubleClicked.connect(self._ques_double_clicked)
        self.questions_list.itemClicked.connect(self._ques_clicked)
        self.delete_ques_button.clicked.connect(self._delete_ques_button_clicked)
        self.show_text_button.clicked.connect(self._show_text_button_clicked)

    def _video_changed(self, idx):
        """
        Функция определяет, что должно происходить при смене видео.

        :param idx: индекс нового выбранного видео.
        :return:
        """
        if idx > -1:
            self.current_sentence = 0
            self.all_sentences = 0
            self.keywords_list_2.setText("")
            self.button_next.setEnabled(False)
            self.button_previous.setEnabled(False)
            self._save_keywords()
            self.words_list.clear()
            self.keywords_list.clear()
            self.questions_list.clear()
            self.words_list.addItems(word for word in self.videos[idx].words if word not in self.videos[idx].keywords)
            self.keywords_list.addItems(self.videos[idx].keywords)
            self.questions_list.addItems(self.videos[idx].questions)
            self.delete_ques_button.setEnabled(False)
            self.show_text_button.setEnabled(True)

    def _show_text_button_clicked(self):
        try:
            idx = self.video_selector_combobox.text_box.currentIndex()
            self.keywords_list_2.setText(self.videos[idx].correct_video_text)

        except Exception:
            msg = QtWidgets.QMessageBox()
            msg.setText("Sorry, an error occured")
            msg.setInformativeText("Please, try again")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()

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
        #self.context_list.clear()

        self.current_sentence = 0
        self.all_sentences = 0
        self.keywords_list_2.setText("")
        self.button_next.setEnabled(False)
        self.button_previous.setEnabled(False)

        idx = self.video_selector_combobox.text_box.currentIndex()
        word = item.text()
        self.sentences = self.videos[idx].correct_video_sentences
        #text = self.videos[idx].text

        self.sentences_idx = self.videos[idx].indexes[self.videos[idx].words.index(word)]

        #for item in sentences_idx:
        #    self.context_list.addItem(sentences[item])

        self.current_sentence = 1
        self.all_sentences = len(self.sentences_idx)

        self.label_count.setText(str(str(self.current_sentence) + "/" + str(self.all_sentences)))

        if self.all_sentences != 1:
            self.button_next.setEnabled(True)

        self.keywords_list_2.setText(self.sentences[self.sentences_idx[0]])

        #pos = text.find(word)
        #while pos > -1:
        #    find_start = pos + 1
        #    start = pos - 50 if pos >= 50 else 0
        #    end = pos + 50 if pos + 50 < len(text) else len(text)
        #    self.context_list.addItem(f'<b>{text[start:end]}</b>')
        #    pos = text.find(word, find_start)

    def _ques_clicked(self, item):
        self.delete_ques_button.setEnabled(True)

    def _ques_double_clicked(self, item):
        self.tb_question.setText(item.text())

    def _delete_ques_button_clicked(self):
        try:
            idx = self.video_selector_combobox.text_box.currentIndex()
            self.videos[idx].questions.remove(self.questions_list.currentItem().text())
            self.questions_list.takeItem(self.questions_list.currentRow())

        except Exception:
            msg = QtWidgets.QMessageBox()
            msg.setText("Sorry, an error occured")
            msg.setInformativeText("Please, try again")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()


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

            window = QtWidgets.QMainWindow()
            window.setWindowTitle("Please, wait")
            ui = Ui_MainWindow()
            ui.setupUi(window)
            window.show()

            try:
                self.videos.add_video(url)
                self._videos_selector_update(len(self.videos) - 1)

            except Exception:
                msg = QtWidgets.QMessageBox()
                msg.setText("Sorry, an error occured")
                msg.setInformativeText("Please, try again")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg.exec_()

            window.close()

        else:
            msg = QtWidgets.QMessageBox()
            msg.setText("Sorry, an error occured")
            msg.setInformativeText("Please, try again")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()

    def _remove_button_clicked(self):
        """
        Функция удаляет видео из списка видео.

        :return:
        """
        idx = self.video_selector_combobox.text_box.currentIndex()
        del self.videos[idx]
        self.words_list.clear()
        self.keywords_list.clear()
        self.keywords_list_2.setText("")
        self._videos_selector_update(idx)
        self.questions_list.clear()

    def _next_button_clicked(self):
        if self.current_sentence == 1:
            self.button_previous.setEnabled(True)
        self.current_sentence += 1
        if self.current_sentence == self.all_sentences:
            self.button_next.setEnabled(False)

        self.label_count.setText(str(str(self.current_sentence) + "/" + str(self.all_sentences)))

        self.keywords_list_2.setText(self.sentences[self.sentences_idx[self.current_sentence-1]])

    def _previous_button_clicked(self):
        if self.current_sentence == self.all_sentences:
            self.button_next.setEnabled(True)
        self.current_sentence -= 1
        if self.current_sentence == 1:
            self.button_previous.setEnabled(False)

        self.label_count.setText(str(str(self.current_sentence) + "/" + str(self.all_sentences)))

        self.keywords_list_2.setText(self.sentences[self.sentences_idx[self.current_sentence - 1]])

    def _button_select_sentence_from_text_clicked(self):
        self.tb_sentence.setText(self.keywords_list_2.toPlainText().replace(".", ""))

    def _button_check_grammar_sentence_clicked(self):
        #return
        #self.tb_sentence.setText(my_tool.correct(self.tb_sentence.toPlainText()))
        self.tb_sentence.setText(grammar_checker.correct_grammar_sentence(self.tb_sentence.toPlainText()))

    def _button_check_grammar_question_clicked(self):
        #return
        #self.tb_question.setText(my_tool.correct(self.tb_question.toPlainText()))
        self.tb_question.setText(grammar_checker.correct_grammar_sentence(self.tb_question.toPlainText()))

    def _button_get_questions_clicked(self):
        questions = question_maker.get_questions(self.tb_sentence.toPlainText())
        if len(questions) == 0:
            msg = QtWidgets.QMessageBox()
            msg.setText("Sorry, we can't create question")
            msg.setInformativeText("Please, try another sentence")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
        else:
            self.tb_question.setText(questions[0])

    def _save_ques_button_clicked(self):
        idx = self.video_selector_combobox.text_box.currentIndex()
        self.videos[idx].questions.add(self.tb_question.toPlainText())
        self.questions_list.addItem(self.tb_question.toPlainText())


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
