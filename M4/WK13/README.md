# fuseAiF_wk13_lstm_text_classification

LSTMs for text classification — Week 13 exercise, FuseAI Fellowship.

## Overview
Builds and trains a simple LSTM classifier on the [AG_NEWS](https://huggingface.co/datasets/fancyzhx/ag_news) dataset to classify headlines into 4 topics: World, Sports, Business, Sci/Tech.

Skeleton notebook — complete the `# TODO` sections (marked `None`) and run top-to-bottom.

## Structure
1. **Vocabulary & Preprocessing** — tokenizer, vocab building from AG_NEWS
2. **Model** — `SimpleLSTM` (embedding → LSTM → FC)
3. **Train & Evaluate** — PyTorch training loop
4. **Reflection** — short conceptual questions
5. **Inference** — classify a new headline

## Usage
Open `LSTMs_for_Text_Classification.ipynb` in Colab or Jupyter, run the first cell to install `datasets`, then run all cells.

## Requirements
- `torch`
- `datasets`

## License
MIT — see [LICENSE](LICENSE).
