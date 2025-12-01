![Na’vi Language Analyzer](https://github.com/user-attachments/assets/7461c8ab-8f12-4dc3-ac64-e39273e24442)

 # :blue_heart: Na’vi Language Analyzer :blue_heart:

*Na'vi sentence analyzer using the dictionary API. The program automatically identifies parts of speech, grammatical characteristics, translation, and creates a visualization of the POS-distribution.*

</div>

## :page_facing_up: Features

- **Linguistic accuracy**: Based on [dict-navi.com](https://dict-navi.com) data 
- **API Integration:** Fetches word data from Navi dictionary API
- **Available without Internet:** Fetches word data from TSV file
- **Data Visualization**: Creates POS distribution baavailabler charts

## :open_file_folder: Installation

```bash
git clone https://github.com/yourusername/naviparser.git
cd naviparser
pip install -r requirements.txt
```

## :computer: Basic Usage 
```python
from NaviParser import NaviParser

parser = NaviParser("config.yaml")

sentence = "Oel ngati kameie, ma tsmukan!"
print(f"Parsing sentence: {sentence}")

df = parser.parse_sentence(sentence)
parser.plot_pos_distribution()
parser.save_results_tsv()

```

## Dependencies
- **requests**: HTTP requests to DictNavi API
- **pandas**: Structured data handling (table output)
- **matplotlib**: POS distribution visualization

<div align="center">
 
*P.S This project is made purely for educational and linguistic research purposes.*

:blue_heart: **Sìlpey oe, fwa tìtweyä ngxìt fìtsengit ohe ngop** :blue_heart:

</div> 
