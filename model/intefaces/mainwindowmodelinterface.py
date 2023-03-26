from common.functions import abstract


class MainWindowModelInterface:
    @abstract
    def getText(self) -> str:
        """Метод возвращает полный текст на английском языке с проверенной грамматикой и пунктуацией."""
        pass

    @abstract
    def getUniqueWords(self) -> list[str]:
        """Метод возвращает список пропаренных (steamed) уникальных слов из текста."""
        pass

    def getWordContexts(self) -> list[str]:
        """
        Функция возвращает контексты слова.
        Нужно сделать так, что бы она возвращала позицию слова...
        """
        pass
