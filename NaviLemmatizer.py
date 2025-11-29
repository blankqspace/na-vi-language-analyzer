import json
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
                print("File is empty, add exceptions.")
                self.lemma_exceptions = {}
        else:
            print("Create exceptions.json")
            self.lemma_exceptions = {}

    def lemmatize(self, word=str) -> str:
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
