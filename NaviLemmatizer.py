import json
from logger import log, logger
from pathlib import Path


class NaviLemmatizer:

    def __init__(self, exceptions_path="exceptions.json"):
        self.case_suffix = ["l", "ìl", "ti", "it", "ru", "ìri", "yä", "ri", "ä"]
        self.verb_suffix = ["ie", "i", "u", "ìm"]
        self.number_prefix = ["ay", "me", "pxe"]

        path = Path(exceptions_path)
        if path.exists():
            try:
                with open("exceptions.json", "r", encoding="utf-8") as f:
                    self.lemma_exceptions = json.load(f)
            except ValueError:
                logger.warning("File is not valid JSON or is empty", path)
                self.lemma_exceptions = {}
        else:
            logger.info("No exceptions file found.")
            self.lemma_exceptions = {}

    @log
    def lemmatize(self, word: str) -> str:
        if not isinstance(word, str):
            raise TypeError("Word must be a string")

        original = word
        word = word.lower()

        for lemma, forms in self.lemma_exceptions.items():
            if word in forms or word == lemma:
                return lemma

        for prefix in self.number_prefix:
            if word.startswith(prefix) and len(word) > len(prefix) + 1:
                word = word[len(prefix) :]
                break

        for suffix in sorted(self.case_suffix, key=len, reverse=True):
            if word.endswith(suffix) and len(word) > len(suffix) + 1:
                word = word[: -len(suffix)]
                break

        for suffix in sorted(self.verb_suffix, key=len, reverse=True):
            if word.endswith(suffix):
                word = word[: -len(suffix)]
                break

        return word
