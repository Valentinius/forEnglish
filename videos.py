import pickle

from video_data import VideoData


class Videos:
    def __init__(self):
        self.videos = []

    def add_video(self, url: str):
        if url not in self.videos:
            self.videos.append(VideoData(url))

    def remove_video(self, url: str):
        self.videos.remove(url)

    def get_names(self):
        """
        Функция возвращает список названий видео.

        :return: список названий видео.
        """
        return [video.name for video in self.videos]

    def get_index(self, name: str):
        """
        Функция возвращает индекс видео по его названию (если оно в списке).

        :param name: название видео.
        :return:
        """
        for i, vid in enumerate(self.videos):
            if vid.name == name:
                return i
        return -1

    def clear(self):
        self.videos.clear()

    def save(self, file_name: str):
        with open(file_name, 'wb') as txt:
            pickle.dump(self.videos, txt)

    def load(self, file_name: str):
        with open(file_name, 'rb') as txt:
            self.videos = pickle.load(txt)

    def __getitem__(self, item):
        return self.videos[item]

    def __setitem__(self, key, value):
        self.videos[key] = value

    def __delitem__(self, key):
        self.videos.pop(key)

    def __len__(self):
        return len(self.videos)

    def __contains__(self, url: str):
        if url in self.videos:
            return True
        return False

    def __iter__(self):
        return iter(self.videos)
