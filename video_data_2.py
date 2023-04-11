import re

from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
#from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk import tokenize
#import nltk
import language_tool_python
import requests
import json

#from gingerit.gingerit import GingerIt
import numpy as np

my_tool = language_tool_python.LanguageTool('en-EN')

class VideoData2:
    def __init__(self, url: str):
        self.url = url
        self.code = re.findall(r'(?<=v=|e/){1}[^\?]+(?=\?{0,1})', url)
        print(self.code)
        self.yt = YouTube(self.url)
        self.subs = YouTubeTranscriptApi.get_transcript(self.code[0], languages=['en'])
        self.name = self.yt.title
        self.duration = self.yt.length
        self.text = self._get_subs_text()
        self.correct_video_text = self._get_correct_video_text()
        self.sentences = tokenize.sent_tokenize(self.correct_video_text)
        #self.correct_video_sentences = self._get_correct_video_sentences()
        self.correct_video_sentences = self.sentences
        self.not_words, self.words, self.indexes = self._get_unique_words()
        self.keywords = list()
        self.questions = set()
        self.done = False

    def _get_subs_text(self):
        """
        Функция получает полный текст из видео.

        :return:
        """
        text = "";
        for i in self.subs:
            text += i['text'] + ' '
        return text

    def _get_correct_video_text(self):
        """
        Функция корректирует полный текст из видео.

        :return:
        """
        #correct_text = my_tool.correct(self.text)
        #url = "https://ginger3.p.rapidapi.com/correctAndRephrase"

        data = {"text": self.text}
        res = requests.post('http://bark.phon.ioc.ee/punctuator', data=data)
        #result = model.restore_punctuation(self.text)

        #querystring = {"text": res.text}
        #headers = {
        #    "X-RapidAPI-Key": "41f7b5275cmsh968b04d97a74f92p18a523jsnb5c26fed1c83",
        #    "X-RapidAPI-Host": "ginger3.p.rapidapi.com"
        #}
        #response = requests.request("GET", url, headers=headers, params=querystring)

        #correct_text = json.loads(response.text)

        result = my_tool.correct(res.text)
        #result = correct_text['data']['text']
        return result

    #def _get_correct_video_sentences(self):
    #    parser = GingerIt()
    #    correct_sentences = []
    #    for sentence in self.sentences:
    #        correct_sentences.append(parser.parse(sentence)['result'])
    #    return correct_sentences

    def _get_unique_words(self):
        """
        Функция находит все уникальные слова в видео.

        :return:
        """

        words = []

        for i in range(len(self.correct_video_sentences)):
            text = self.correct_video_sentences[i].lower()
            words_1 = np.array(text.split())
            words_1 = [word.strip('.,!;()[]') for word in words_1]
            words_1 = [word.replace("'s", '') for word in words_1]
            words_1 = [[word, i] for word in words_1]
            words += words_1

        english_stops = set(stopwords.words('english'))

        unique_words = []
        sentences_indices = []
        for word in words:
            if word[0] not in unique_words:
                if word[0] not in english_stops:
                    unique_words.append(word[0])
                    sentences_indices.append([word[1]])
            else:
                if word[1] not in sentences_indices[unique_words.index(word[0])]:
                    sentences_indices[unique_words.index(word[0])].append(word[1])

        words_without_stops = unique_words

        words_without_stops, sentences_indices = zip(*sorted(zip(words_without_stops, sentences_indices)))

        return words, words_without_stops, sentences_indices

    def __eq__(self, other):
        if type(other) == VideoData2 and self.url == other.url:
            return True
        elif type(other) == str and self.url == other:
            return True
        return False