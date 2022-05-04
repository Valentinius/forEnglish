import re

from pytube import YouTube
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


class VideoData:
    def __init__(self, url: str):
        self.url = url
        self.yt = YouTube(self.url)
        self.name = self.yt.title
        self.duration = self.yt.length
        self.text = self._get_subs_text()
        self.words = self._get_unique_words()
        self.keywords = set()
        self.questions = set()
        self.done = False

    def _get_subs_text(self):
        """
        Функция получает полный текст из видео.

        :return:
        """
        caption = self.yt.captions.get_by_language_code('a.en')
        xml_string = caption.xml_captions

        words = list(re.findall(r'>\s*([a-z\s]+)</s>', xml_string))
        return ' '.join(words)

    def _get_unique_words(self):
        """
        Функция находит все уникальные слова в видео.

        :return:
        """
        caption = self.yt.captions.get_by_language_code('a.en')
        xml_string = caption.xml_captions

        words = set(re.findall(r'>\s*([a-z\s]+)</s>', xml_string))

        word_stemmer = PorterStemmer()
        steamed_words = set([word_stemmer.stem(word) for word in words])

        english_stops = set(stopwords.words('english'))
        words_without_stops = set([word for word in steamed_words if word not in english_stops])

        return words_without_stops

    def __eq__(self, other):
        if type(other) == VideoData and self.url == other.url:
            return True
        elif type(other) == str and self.url == other:
            return True
        return False
