import os
import yaml
import pandas as pd
import requests
import matplotlib.pyplot as plt

from abc import ABC, abstractmethod
from logger import logger, log
from NaviLemmatizer import NaviLemmatizer
from typing import List, Dict, Any


class AbstractProvider(ABC):
    def __init__(self, url: str, timeout: int, retries: int):
        self.url = url
        self.timeout = timeout
        self.retries = retries

    @abstractmethod
    def load(self) -> List[Dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def extract_word_info(self, item: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError


class TSVProvider(AbstractProvider):
    def __init__(self, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"TSV file not found.")
        super().__init__(url="", timeout=0, retries=0)
        self.file_path = file_path

    def load(self) -> List[Dict[str, Any]]:
        try:
            df = pd.read_csv(self.file_path, sep="\t")
            if not all(
                col in df.columns for col in ["Word (Na'vi)", "POS", "Translation (en)"]
            ):
                logger.warning("TSV file missing expected columns")
                return []

            data_list = []
            for i, row in df.iterrows():
                item = {
                    "navi": str(row["Word (Na'vi)"]).strip().lower(),
                    "pos": str(row["POS"]).strip(),
                    "translations": [str(row["Translation (en)"]).strip()],
                    "syllabic": "",
                    "acoustic": "",
                }
                data_list.append(item)
            return data_list
        except Exception as e:
            logger.exception(f"Failed to read TSV file: {e}")
            return []

    def extract_word_info(self, item: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "navi": item.get("navi", ""),
            "syllabic": item.get("syllabic", ""),
            "acoustic": item.get("acoustic", ""),
            "pos": item.get("pos", "unknown"),
            "translations": item.get("translations", []),
        }


class DictNaviProvider(AbstractProvider):

    def load(self) -> List[Dict[str, Any]]:
        for attempt in range(self.retries):
            try:
                logger.info(f"Loading DictNavi API (attempt {attempt+1})")
                response = requests.get(self.url, timeout=self.timeout)
                response.raise_for_status()
                data = response.json()
                if not isinstance(data, list):
                    logger.warning(
                        "DictNavi returned non-list response; expected list."
                    )
                    return []
                return data
            except Exception as e:
                logger.warning(f"DictNavi load failed: {e}")
        logger.error("DictNavi API unreachable")
        return []

    def extract_word_info(self, item: Dict[str, Any]) -> Dict[str, Any]:
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
        self.lemmatizer = NaviLemmatizer()

        provider_cfg = self.config.get("provider", {})
        provider_type = provider_cfg.get("type", "").lower()

        if provider_type == "tsv":
            tsv_path = provider_cfg.get("tsv_path")
            if not tsv_path or not os.path.exists(tsv_path):
                raise FileNotFoundError(f"TSV file not found: {tsv_path}")
            self.provider: AbstractProvider = TSVProvider(tsv_path)
        elif provider_type == "api":
            url = provider_cfg.get("api_url")
            timeout = provider_cfg.get("timeout")
            retries = provider_cfg.get("retry_attempts")
            if not url:
                raise ValueError("API URL must be specified in config.yaml")
            self.provider: AbstractProvider = DictNaviProvider(url, timeout, retries)
        else:
            raise ValueError(f"Unknown provider type: {provider_type}")

        logger.info(f"Using provider: {provider_type}")
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
    parser = NaviParser("config.yaml")

    sentence = "Oel ngati kameie, ma tsmukan!"
    print(f"Parsing sentence: {sentence}")

    df = parser.parse_sentence(sentence)
    print("\nResulting DataFrame:")
    print(df)
    parser.plot_pos_distribution()
    parser.save_results_tsv()
