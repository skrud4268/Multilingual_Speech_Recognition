# Multilingual Speech Recognition Project

## Project Overview

In the realm of artificial intelligence, understanding multilingual sentences in audio clips presents a significant challenge. Current technologies like Siri, Alexa, and Google Nest are limited to understanding and performing tasks in a single pre-set language. Our project aims to advance these technologies, enabling them to comprehend and converse in multiple languages within the same sentence, thereby making interactions with AI more human-like.

## Objectives

The goal of this project is to develop a speech recognition system that can classify and identify languages at the word level in multilingual sentences. Using deep learning techniques and machine learning models, we aim to fine-tune a pre-trained wav2vec model with a custom dataset in WAV format. The objective is to enhance the model's ability to decode and process mixed-language audio clips efficiently.

### Specific Goals

- Create a dataset for audio sequence classification in multilingual sentences.
- Fine-tune a pre-trained wav2vec model with this dataset.
- Evaluate the performance of the model.

## How to Run the Code

### Prerequisites

- Python environment with necessary libraries installed.
- Access to a GPU for training (can use Google Colab with GPU runtime).

### Setup and Execution

1.  **Preparing the Data:**

    Files: `Koreanfood_data.py`, `sentence_to_word.py`

    - These scripts break down sentences into word-level segments, convert them to WAV format using TTS, and store them in the `segments` folder.
    - Each segment is labeled as either English or Korean, and a CSV file containing the segment audio file names and their corresponding labels is generated.
    - The individual segment audio files are merged with a 400-millisecond pause between them to form sentence audio files, which are stored in the `sentences` folder.

2.  **Fine-Tuning the Model:**

    File: `Multilingual.ipynb`

    - Utilizes the audio files and labels from the `segments` folder for model training.
    - Installation of required packages:

      ```bash
      pip install accelerate -U
      pip3 install datasets
      ```

    - Important imports:

      ```python
      import torch
      from transformers import AutoProcessor, Wav2Vec2ForSequenceClassification, TrainingArguments, Trainer
      from datasets import Dataset, DatasetDict, load_metric
      import librosa
      import pandas as pd
      from sklearn.model_selection import train_test_split
      ```

    - Load the CSV File and Create a Mapping Dictionary:

      - A CSV file, presumably containing filenames and their corresponding language labels, is loaded into a pandas DataFrame.
      - A dictionary (file_label_map) is created to map filenames to their respective language labels.

    - Define a Function to Map Label Text to Integer:

      - A dictionary (label_to_id) is defined to map language labels (in this case, "English" and "Korean") to integer values. This is a common practice in machine learning to handle categorical data.

    - Load Model and Processor:

      - A processor (AutoProcessor) and a model (Wav2Vec2ForSequenceClassification) are loaded from Hugging Face's model hub.
      - The processor is specific to the facebook/wav2vec2-base model, which is a popular choice for audio processing tasks.
      - The model is also loaded from the facebook/wav2vec2-base but is configured for sequence classification with two labels (as indicated by num_labels=2).

    - Preprocess Audio Files: A function is defined to load and preprocess audio files using librosa. It reads audio files, processes them with a specified processor, and prepares input values and labels for each file.

    - Prepare and Split Dataset:
      - The dataset paths are prepared by appending a directory prefix to filenames.
      - The dataset is split into training and validation sets using train_test_split, with 20% of data reserved for validation.
    - Convert DataFrames to Datasets and Apply Preprocessing:
      - DataFrames containing file paths for training and validation sets are converted to Hugging Face Datasets.
      - The preprocessing function is applied to these datasets in a batched manner.
      - A DatasetDict is created containing both the training and validation datasets.
    - Define Training Arguments and Initialize Trainer:
      - Training arguments are defined with specific settings for batch size, gradient accumulation, evaluation strategy, number of epochs, saving and evaluation steps, learning rate, and weight decay.
      - A Trainer is initialized with the model, training arguments, datasets, and tokenizer/feature extractor.

3.  **Model Evaluation:**

    - After training, save the model and processor.
    - Load the model, the processor, and the validation dataset.
    - Perform predictions on the validation dataset and generate a classification report and confusion matrix.

### Example Code Snippet for Evaluation

```python
import torch
from transformers import AutoProcessor, Wav2Vec2ForSequenceClassification, Trainer
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd
from datasets import load_dataset

# Load model and processor
model_path = './saved_wav2vec2_model'
model = Wav2Vec2ForSequenceClassification.from_pretrained(model_path)
processor = AutoProcessor.from_pretrained(model_path)

# Initialize Trainer
trainer = Trainer(model=model, tokenizer=processor.feature_extractor)

# Perform predictions and generate report
# ... (code for prediction and evaluation)
```
