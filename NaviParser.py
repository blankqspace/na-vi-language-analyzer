import os
import yaml
import pandas as pd
import requests
import matplotlib.pyplot as plt

from logger import logger, log
from NaviLemmatizer import NaviLemmatizer


class DictNaviProvider:

    def __init__(self, url, timeout, retries):
        self.url = url
        self.timeout = timeout
        self.retries = retries

    def load(self):
        for attempt in range(self.retries):
            try:
                logger.info(f"Loading DictNavi API (attempt {attempt+1})")
                response = requests.get(self.url, timeout=self.timeout)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.warning(f"DictNavi load failed: {e}")
        logger.error("DictNavi API unreachable")
        return []

    def extract_word_info(self, item):
        return {
            "navi": item.get("navi", ""),
            "syllabic": item.get("syllabic", ""),
            "acoustic": item.get("acoustic", ""),
            "pos": item.get("wordclass", "unknown"),
            "translations": item.get("translations", []),
        }


class NaviParser:
    def __init__(self, config_path="config.yaml"):
        self.config = yaml.safe_load(open(config_path, "r", encoding="utf-8"))

        timeout = self.config["api"]["timeout"]
        retries = self.config["api"]["retry_attempts"]

        url = "https://dict-navi.com/api/list"

        self.provider = DictNaviProvider(url, timeout, retries)
        self.lemmatizer = NaviLemmatizer()

        logger.info("Using provider: dict_navi")
        self.data_list = self.provider.load()

        self.results = []

    @log
    def tokenize(self, sentence):
        return [w.strip(".,!?") for w in sentence.split()]

    @log
    def get_word_info(self, word):
        lemma = self.lemmatizer.lemmatize(word.lower())

        match = next(
            (item for item in self.data_list if item.get("navi", "").lower() == lemma),
            None,
        )

        if match:
            return self.provider.extract_word_info(match)

        return {
            "navi": word,
            "syllabic": "",
            "acoustic": "",
            "pos": "unknown",
            "translations": [],
        }

    @log
    def parse_sentence(self, sentence):
        tokens = self.tokenize(sentence)
        self.results = [self.get_word_info(t) for t in tokens]
        return pd.DataFrame(self.results)

    @log
    def save_results_tsv(self, filename="results.tsv"):

        if not self.results:
            print("No results to save.")
            return

        os.makedirs("tsv files output", exist_ok=True)
        file_path = os.path.join("tsv files output", filename)

        df = pd.DataFrame(self.results)
        df.to_csv(file_path, sep="\t", index=False, encoding="utf-8")
        logger.info(f"Results saved to {file_path}")

    @log
    def plot_pos_distribution(self):
        if not self.results:
            print("There's no data for plot creation.")
            return

        df = pd.DataFrame(self.results)
        counts = df["pos"].value_counts()

        os.makedirs("pos_distributions", exist_ok=True)
        file_path = os.path.join("pos_distributions", "pos_distribution.png")

        plt.bar(counts.index, counts.values)
        plt.xlabel("POS")
        plt.ylabel("Quantity")
        plt.title("POS distribution")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(file_path)
        plt.close()


if __name__ == "__main__":
    parser = NaviParser()

    sentence = "Oel ngati kameie, ma tsmukan!"
    print(f"Parsing sentence: {sentence}")

    df = parser.parse_sentence(sentence)
    print("\nResulting DataFrame:")
    print(df)
    parser.plot_pos_distribution()
    parser.save_results_tsv()
