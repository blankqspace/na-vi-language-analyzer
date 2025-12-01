import pytest
from unittest.mock import MagicMock
from NaviLemmatizer import NaviLemmatizer
from NaviParser import NaviParser


def test_lemmatize_simple():

    lemmatizer = NaviLemmatizer()

    # number
    assert lemmatizer.lemmatize("pxetsmukan") == "tsmukan"
    # case
    assert lemmatizer.lemmatize("tìyawnä") == "tìyawn"
    # verb
    assert lemmatizer.lemmatize("kameie") == "kame"


@pytest.fixture
def parser():
    p = NaviParser.__new__(NaviParser)
    p.lemmatizer = NaviLemmatizer()
    p.provider = MagicMock()
    p.provider.extract_word_info.side_effect = lambda item: {
        "navi": item["navi"],
        "syllabic": item.get("syllabic", ""),
        "acoustic": item.get("acoustic", ""),
        "pos": item.get("wordclass", "unknown"),
        "translations": item.get("translations", []),
    }

    p.data_list = [
        {
            "navi": "oel",
            "syllabic": "o-el",
            "acoustic": "",
            "wordclass": "noun",
            "translations": ["hello"],
        },
        {
            "navi": "ngati",
            "syllabic": "nga-ti",
            "acoustic": "",
            "wordclass": "pronoun",
            "translations": ["you"],
        },
    ]

    return p


def test_tokenize(parser):
    tokens = parser.tokenize("Oel ngati kameie, ma tsmukan!")
    assert tokens == ["Oel", "ngati", "kameie", "ma", "tsmukan"]


def test_get_word_info_found(parser):
    parser.lemmatizer.lemmatize = lambda w: "ngati"
    info = parser.get_word_info("ngati")
    assert info["navi"] == "ngati"
    assert info["pos"] == "pronoun"
    assert info["translations"] == ["you"]


def test_get_word_info_not_found(parser):
    parser.lemmatizer.lemmatize = lambda w: w
    info = parser.get_word_info("unknownword")
    assert info["navi"] == "unknownword"
    assert info["pos"] == "unknown"
    assert info["translations"] == []
