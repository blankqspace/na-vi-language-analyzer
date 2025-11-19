![navi parser](https://github.com/user-attachments/assets/7461c8ab-8f12-4dc3-ac64-e39273e24442)

 # :blue_heart: Na'vi Language Grammar Parser :blue_heart:

*A Python-based library for grammatical analysis and morphological processing of the Na'vi language from James Cameron's Avatar universe*

</div>

## :page_facing_up: Features

- **Tokenization**: Breaks down Na'vi text into individual words with grammatical analysis
- **Part-of-Speech Tagging**: Identifies word types (nouns, verbs, pronouns, adjectives, particles, prenouns, numbers)
- **Syntax Processing**: Analyzes sentence types (declarative, interrogative, imperative, exclamative), identifies constituents (noun phrases, verb phrases)
- **Visualization**: Creates POS distribution charts with pie and bar graphs
- **Unified Reporting**: Generates comprehensive analysis reports in text format

## Linguisctic features
**Supported Parts-of-speech**
- **NOUN** - Nouns with case, number, and gender analysis
- **VERB** - Verbs with transitivity and tense analysis  
- **PRONOUN** - Personal pronouns with person and case
- **ADJECTIVE** - Descriptive adjectives
- **PARTICLE** - Grammatical particles (vocative, conjunctions, etc.)
- **PRENOUN** - Determiners and modifiers
- **NUMBER** - Numerical values

**Syntax Analysis**
- Identifies constituents: noun phrases (NP) and verb phrases (VP)
- Analyzes sentence structure and purpose analysis
- **Certainty Level**: High, medium, or low based on linguistic markers
- **Emotional Tone**: Positive, negative, or neutral

## :pencil2: Error Handling
The parser includes custom error handling:
- **InvalidInputError**: Empty or invalid text input
- **TokenizationError**: Word processing issues
- **WordClassificationError**: Word type identification failures

## :open_file_folder: Installation

```bash
git clone https://github.com/your-username/navi-parser.git
cd navi-parser
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## :computer: Basic Usage 
```python
from facade import NaviParserFacade, Configuration

# Create parser with default settings
config = Configuration(
    use_linguistic_analysis=False,  # Disable spaCy dependency
    enable_visualization=True,      # Enable visualizations
    save_plots=True,               # Save plot files
    output_dir="navi_analysis_output"
)

parser = NaviParserFacade(config)

# Analyze a sentence
result = parser.analyze_sentence("Oel ngati kameie ma tsmukan?")
```
## :hourglass: Examples

### Basic Analysis
```python
from facade import NaviParserFacade, Configuration

parser = NaviParserFacade()
result = parser.analyze_sentence("Tsrulen oeru ti txan")
```
### Batch Analysis
```python
sentences = [
    "Oel ngati kameie",
    "Tsrulen oeru ti txan",
    "Irayo oer prrnen"
]

results = parser.analyze_multiple_sentences(sentences)
```

## Dependencies
- **numpy**: Numerical operations for visualization
- **matplotlib**: Chart and plot generation
- **networkx**: Graph structures (for future dependency tree features)
  
## Notes
- The parser works without spaCy by default to avoid model dependencies
- Linguistic analysis can be enabled for enhanced features
- All output files are saved to the specified output directory

<div align="center">
 
*P.S This project is made purely for educational and linguistic research purposes.*

</div> 
