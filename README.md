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

    Files: `sentence_to_word.py`

    - This script break down sentences into word-level segments, convert them to WAV format using TTS, and store them in the `segments` folder.
    - Each segment is labeled as either English or Korean, and a CSV file containing the segment audio file names and their corresponding labels is generated.
    - The individual segment audio files are merged with a 400-millisecond pause between them to form sentence audio files, which are stored in the `sentences` folder.

    Files: `koreanfood_data.py`, `englishfood_data.py`, `koreanhobby_data.py`, `englishhobby_data.py`

    - These scripts are used to generate datasets that supplement the main dataset, particularly when it's challenging to create sentences with more than one language using sentence_to_word.py.
    - Each of these files generates sentences in a simple format, where the dominant language contains a single word from the non-dominant language.
    - By incorporating 100 different words, they generate 100 distinct sentences.
    - Since each of these codes generates its own labeled data, manual merging of the CSV files is required to utilize all datasets.
    - Otherwise functions similar to `sentence_to_word.py`

2.  **Fine-Tuning the Model & Evaluation:**

    File: `Multilingual.ipynb`

    - Utilizes the audio files from the `segments` folder and labels for model training.
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

    - Evaluation:
      - After training, save the model and processor.
      - Load the model, the processor, and the validation dataset.
      - Perform predictions on the validation dataset and generate a classification report and confusion matrix.

3.  **Additional Code:**

    File: `autosplit.py`

    - This code is designed to break down sentences into segments based on silent duration.
    - It is written for use in sequence labeling, where sentence audio files are input into a trained audio classification model.
    - The criterion for segmentation is the silent duration, and in this case, the code uses a standard of 400 milliseconds. This duration can be adjusted as needed.

## Conclusion:

In our project, we've innovated in the field of multilingual speech recognition by creating datasets from text sentences alone, addressing the lack of readily available resources. Our method automates audio file labeling and conversion, a crucial step for scarce multilingual datasets. We introduced a novel technique for merging audio segments into cohesive sentences, using a 400-millisecond pause as a segmentation indicator. While this approach simplifies natural language processing, it's a stepping stone towards more advanced methods.

Our future endeavors aim to enhance AI's comprehension of multilingual contexts. We plan to develop a custom model for sequence labeling, focusing on sentence-level audio analysis, thus advancing conversational AI systems. This work represents not only a technological advancement but also a move towards more inclusive AI-human interactions in diverse linguistic environments.
